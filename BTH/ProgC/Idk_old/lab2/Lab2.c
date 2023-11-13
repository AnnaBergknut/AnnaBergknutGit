// 1280x720, MJPG
//steg0
#include <stdio.h>              // Standard input/output (printf)
#include <stdlib.h>             // Standard library
#include <string.h>             // C string operations
#include <unistd.h>             // close device handle
#include <fcntl.h>              // open device handle
#include <errno.h>              // check errors
#include <sys/ioctl.h>          // icotl (read/write to driver)
#include <sys/stat.h>           // stat  (get file descriptor info)
#include <sys/mman.h>           // memory maps
#include <linux/videodev2.h>    // camera driver interface
#include <math.h>

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"
#include "jpegutils.c"

#include <SDL2/SDL.h>           // step 0 lab2
#include <omp.h>                // steg 3 lab2

#define MIN(a, b) (((a) < (b)) ? (a) : (b))
#define MAX(a, b) (((a) < (b)) ? (b) : (a))

#define CAM_WIDTH 640
#define CAM_HEIGHT 360


// The struct Pixel holdes the information for every pixel in the picture
typedef struct Pixel 
{
    unsigned char R;
    unsigned char G;
    unsigned char B;
    unsigned char A;

} Pixel;

//This funktion converts the given pixel from a YUYV format to a RGB format
// This is the formula to convert yuyv to rgb, the u and v are the colors represented and the
// two different y are black and white.
int YUYVtoRGB(unsigned char y, unsigned char u, unsigned char v, Pixel* _rgba)
{
    int c = y - 16;
    int d = u - 128;
    int e = v - 128;

    int red = MAX(0, MIN((298 * c + 516 * d + 128) >> 8, 255));
    int green = MAX(0, MIN((298 * c - 100 * d - 208 * e + 128) >> 8, 255));
    int blue = MAX(0, MIN((298 * c + 409 * e + 128) >> 8, 255));
    // this is the acutual convertion funktions in order to get rgb from uv.
    _rgba->A = 255; //Alpha
    _rgba->B = blue;
    _rgba->G = green;
    _rgba->R = red;
    
    if(blue>=250 && green>=250 && red>=250)
    {
       return 1;
    } 
    return 0;
}


int coordinates ( int xVal, int yVal)
{
    if( yVal < (CAM_HEIGHT/4))
    {
        printf("Back \n");
    }
    else if( xVal < (CAM_WIDTH/4))
    {
        printf("Left \n");
    }
    else if(xVal > (CAM_WIDTH-(CAM_WIDTH/4)))
    {
        printf("Right \n");
    }
    else
    {
        printf("Forward \n");
    }
    return 0;
}


int ProcessImage(const unsigned char *mjpeg, int size, void *pixels)
{
    // This funktion prosseses the image both calls the function to konvert the image from yuyv
    // to rgb, calls add circle function and saves the image
    #define RGB_SIZE CAM_WIDTH * CAM_HEIGHT

    // the following 4 rows adds the right amount of Pixels in the varibles rgbConversion, Y, 
    // U and V
    Pixel* rgbConversion = (Pixel*)pixels;
    

    //static Pixel rgbConversion[RGB_SIZE];

    static unsigned char Y[RGB_SIZE];

    static unsigned char U[RGB_SIZE];

    static unsigned char V[RGB_SIZE];

    // jpeg is another color formate and this funktion decodes it. This do to my pc only 
    // suporting MJPG not YUYV. So the function decodes the MJPG formate to YUYV format
    // the varibels Y U and V are inputs, and will there for be loaded with there data
    int result = decode_jpeg_raw((unsigned char*)mjpeg, size, 0, Y4M_CHROMA_422, CAM_WIDTH, CAM_HEIGHT, Y, U, V);


    if(result != 0){
        printf("Error in decode_jpeg_raw: %d\n",result);
    }

    int yuvSize = (CAM_WIDTH) * (CAM_HEIGHT) /2;

    double t0 = omp_get_wtime();
    // This for loop puts all the data step by step in varibles to then call the function 
    // YUYVtoRGB function to convert the data
    int stop = 0;
    int threads = 11;
    #pragma omp parallel num_threads(threads)
    {
        int id = omp_get_thread_num();
        
        int yIndex=2*id;

        int uIndex=id;

        int vIndex=id;
        
        int rgbIndex = 2*id;

        int found = 0;

        for (int i = id; i < yuvSize; i += threads)
        {

            unsigned char y1 = Y[yIndex++];
            unsigned char u = U[uIndex];
            unsigned char y2 = Y[yIndex];
            unsigned char v = V[vIndex];


            if (YUYVtoRGB(y1, u, v, &rgbConversion[rgbIndex++])== 1 && found == 0)
            {
                found = 1;
            }
            if(YUYVtoRGB(y2, u, v, &rgbConversion[rgbIndex]) == 1 && found == 0)
            {
                found = 1;
            }
            uIndex += threads;
            vIndex += threads;
            yIndex += (2*threads)-1;
            rgbIndex += (2*threads)-1;

            if (found == 1 && stop == 0)
            {  
                stop = 1;
                int index = rgbIndex;
                int xVal = index%CAM_WIDTH;
                int yVal = floor(index/CAM_HEIGHT);
                coordinates (xVal, yVal);
                found = 2;
            }

        }
    }
    double milliseconds = (omp_get_wtime() - t0) * 1000;

    printf("Time spent: %5.2fms\r", milliseconds);
    return floor(milliseconds);
}

int bufMap(int *cameraHandle, unsigned char* *imageMemory, struct v4l2_buffer *buf_prt)
{
    // forloop in orther to run it twice inother to get 2 buffers.
    int i;
    for (i = 0; i < 2; i++)
    {
        // create the buffer and sets the memeroy to 0 and decler typ and size. 
        struct v4l2_buffer buf;
        memset(&buf, 0, sizeof(buf));
        buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE; // we tell what the type will do. will make use of this in step 7
        buf.memory = V4L2_MEMORY_MMAP;
        buf.index = i;

        if (ioctl(*cameraHandle, VIDIOC_QUERYBUF, &buf) < 0)
        {
            printf("VIDIOC_QUERYBUF failed!\n");
            return -1;
        }

        if(ioctl(*cameraHandle, VIDIOC_QBUF, &buf) < 0)
        {
            printf("VIDIOC_QBUF failed!\n");
            return -1;
        }

        // create a private mapping into the driver memerory for imagememeroy 
        // this means that later on when we dq the buffer the imagedata will be placed in imagememery
        imageMemory[i] = mmap(NULL, buf.length, PROT_READ, MAP_SHARED, *cameraHandle, buf.m.offset);
        buf_prt[i] = buf;
    }
    return 0;
}

int startCamera(int *cameraHandle)
{
    // starts the camera and and q the bufin oder to fill with imagedata
    // type starts
    enum v4l2_buf_type type = V4L2_BUF_TYPE_VIDEO_CAPTURE;

    if (ioctl(*cameraHandle, VIDIOC_STREAMON, &type) < 0)
    {
        printf("VIDIOC_STREAMON failed!\n");
        return -1;
    }
    
    return 0;
}
    
int allocateMemory(int *cameraHandle)
{
    // allocate the memery needed for the image data and create the mapping
    struct v4l2_requestbuffers req;
    memset(&req, 0, sizeof(req));
    req.count = 2;
    req.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    req.memory = V4L2_MEMORY_MMAP;

    if (ioctl(*cameraHandle, VIDIOC_REQBUFS, &req) < 0)
    {
        printf("VIDIOC_REQBUFS failed!\n");
        return -1;
    }
    return 0;
}

int formate(int *cameraHandle)
{
    // declearade the formate that we will use for the camera. such as the pixels and dimantions of the camera.
    struct v4l2_format format;
    memset(&format,0,sizeof(format));
    format.type = V4L2_BUF_TYPE_VIDEO_CAPTURE; 
    format.fmt.pix.width = CAM_WIDTH; 
    format.fmt.pix.height =CAM_HEIGHT; 
    format.fmt.pix.pixelformat = V4L2_PIX_FMT_YUYV;
    format.fmt.pix.field = V4L2_FIELD_ANY;

    if (ioctl(*cameraHandle, VIDIOC_S_FMT, &format) < 0)
    {
        printf("VIDIOC_S_FMT Video format set fail\n");
        return -1;
    }
    return 0;
}

int deque(int *cameraHandle, struct v4l2_buffer *buf_prt, int index)
{
    if (ioctl(*cameraHandle, VIDIOC_DQBUF, &buf_prt[index]) < 0) 
        {
            return errno;
        }
}

int enque(int *cameraHandle, struct v4l2_buffer *buf_prt, int index)
{
    // q up the buffer again in order for easy restart
    if (ioctl(*cameraHandle, VIDIOC_QBUF, &buf_prt[index]) < 0)
    {
        printf("VIDIOC_QBUF failed!\n");
        return -1;
    }
}

int main()
{
    float sum = 0;
    int times = 0;
    // variblels
    unsigned char* imageMemory[2];                          // the array that wil store the pixels.
    struct v4l2_buffer bufs[2];

    int cameraHandle = open("/dev/video0", O_RDWR, 0);      // find the camera

    formate(&cameraHandle);
    
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *g_window = SDL_CreateWindow("SDL Window", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, CAM_WIDTH, CAM_HEIGHT, SDL_WINDOW_OPENGL | SDL_WINDOW_SHOWN);
    SDL_Renderer *g_renderer = SDL_CreateRenderer(g_window, -1, SDL_RENDERER_ACCELERATED);
    SDL_Texture *g_streamTexture = SDL_CreateTexture(g_renderer, SDL_PIXELFORMAT_ARGB8888, SDL_TEXTUREACCESS_STREAMING, CAM_WIDTH, CAM_HEIGHT);

    void *pixels;
    int pitch;

    allocateMemory(&cameraHandle);
    
    bufMap(&cameraHandle,imageMemory, bufs);

    startCamera(&cameraHandle);
   
    SDL_Event event;
    int idx = 0;

    while (1)
    {
        if (SDL_PollEvent(&event))
        {
            if (event.type == SDL_KEYDOWN)
            {
                if (event.key.keysym.sym == SDLK_ESCAPE)
                {
                    float avg = sum/times;

                    printf("I exit Multi now\n The avg time is %f \n", avg);

                    close(cameraHandle);
                    SDL_DestroyRenderer(g_renderer);
                    SDL_DestroyWindow(g_window);
                    SDL_Quit();

                    return 0;
                }
            }
        }
        SDL_LockTexture(g_streamTexture, NULL, &pixels, &pitch);

        deque(&cameraHandle, bufs, idx);

        int milsec;
        milsec = ProcessImage(imageMemory[bufs[idx].index], bufs[idx].bytesused, pixels);

        sum += milsec;
        times += 1;

        enque(&cameraHandle, bufs, idx);

        SDL_UnlockTexture(g_streamTexture);

        SDL_RenderCopy(g_renderer, g_streamTexture, NULL, NULL);

        SDL_RenderPresent(g_renderer);


        if(idx == 0)
        {
            idx = 1;
        }
        else
        {
            idx = 0;
        }
    }

    return 0;

}