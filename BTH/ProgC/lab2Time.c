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

#include <SDL2/SDL.h>           // step 0 lab2
#include <omp.h>                // steg 3 lab2

#define MIN(a, b) (((a) < (b)) ? (a) : (b))
#define MAX(a, b) (((a) < (b)) ? (b) : (a))

#define CAM_WIDTH 640
#define CAM_HEIGHT 360
#define RGB_SIZE CAM_WIDTH * CAM_HEIGHT

// The struct Pixel holdes the information for every pixel in the picture
typedef struct Pixel 
{
    unsigned char R;
    unsigned char G;
    unsigned char B;
    unsigned char A;

} Pixel;

typedef struct Time
{
    double image;
    double laser;
} Time;


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
    
    return 0;
}


int coordinates (int idx)
{
    if(idx >= (RGB_SIZE/3)*2)
    {
        printf("Back \n");
    }
    else if(idx%CAM_WIDTH < (CAM_WIDTH/4))
    {
        printf("Left \n");
    }
    else if(idx%CAM_WIDTH > (CAM_WIDTH-(CAM_WIDTH/4)))
    {
        printf("Right \n");
    }
    else
    {
        printf("Forward \n");
    }
    return 0;
}


int laser(Pixel* rgbConversion)
{
    int high_score;
    high_score = 0;
    int coordinate;

    int score;
    int check = 0;
    int pix = 10;
    

    for (int i = 0; i<RGB_SIZE; i++)
    {
        score = 0;
        //check = 0;
        
        if (rgbConversion[i].R>=200 && rgbConversion[i].B<=150 && rgbConversion[i].G<=150)
        {
            //printf("red\n");
            check = 1;
        }

        
        if (rgbConversion[i].B>=250 && rgbConversion[i].G>=250 && rgbConversion[i].R>=250)
        {
            
            for (int j = -pix; j <=pix; j++)
            {
                if ((i+j <= RGB_SIZE) || (i+j >= 0))
                {
                    if (rgbConversion[i+j].B>=250 && rgbConversion[i+j].G>=250 && rgbConversion[i+j].R>=250)
                    {
                        score += 5;
                    }
                    if (rgbConversion[i+j].R==200 && rgbConversion[i+j].B<=150 && rgbConversion[i+j].G<=150)
                    {
                        printf("red p\n");
                        score += 20;
                        //check = 1;
                    }
                }

                if ((i+(j*CAM_WIDTH) <= RGB_SIZE) || (i+(j*CAM_WIDTH) >= 0))
                {
                    if (rgbConversion[i+(j*CAM_WIDTH)].B>=250 && rgbConversion[i+(j*CAM_WIDTH)].G>=250 && rgbConversion[i+(j*CAM_WIDTH)].R>=250)
                    {
                        score += 5;
                    }
                    if (rgbConversion[i+(j*CAM_WIDTH)].R==200 && rgbConversion[i+(j*CAM_WIDTH)].B<=150 && rgbConversion[i+(j*CAM_WIDTH)].G<=150)
                    {
                        printf("red p\n");
                        score += 20;
                        //check = 1;
                    }
                }

                
            }
            
            /*if (check == 0)
            {
                score = 0;
            }*/

            

            if (high_score < score)
            {
                coordinate = i;
                high_score = score;
            }


        }
    }


    if (high_score > 0 && check == 1)
    {
        coordinates(coordinate);
    }
    
    return 0;
}

// this funktion prosess the image so that it wil be on rgb and call on the funktion to draw the circle. 
Time ProcessImage(const unsigned char* _yuv, int _size, void* pixels, int numThreads)
{
    Time times;
    static double laser_milliseconds = 0;
    static double image_milliseconds = 0;

    double t0 = omp_get_wtime();

    Pixel* rgbConversion = (Pixel*)pixels;

    #pragma omp parallel num_threads(numThreads)
    {
        int thread_num = omp_get_thread_num();
        int chunk_size = _size / numThreads; // Divide the work evenly among threads
        int start = thread_num * chunk_size; // Calculate the starting index for this thread
        int end = (thread_num == numThreads - 1) ? _size : start + chunk_size; // Calculate the ending index

        for (int i = start; i < end; i += 4)
        {
            unsigned char y1 = _yuv[i + 0];
            unsigned char u = _yuv[i + 1];
            unsigned char y2 = _yuv[i + 2];
            unsigned char v = _yuv[i + 3];

            int rgbIndex = 2 * (i / 4);

            YUYVtoRGB(y1, u, v, &rgbConversion[rgbIndex]);
            YUYVtoRGB(y2, u, v, &rgbConversion[rgbIndex + 1]);
        }
    }
    double image_s = (omp_get_wtime() - t0) * 1000;
    times.image = image_s;
    printf("image time: %5.2fms\n", image_s);

    double lt0 = omp_get_wtime();
    laser(rgbConversion);
    double laser_s = (omp_get_wtime() - lt0) * 1000;
    times.laser = laser_s;
    printf("laser time: %5.2fms\n", laser_s);

    return times;
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
    return 0;
}

int enque(int *cameraHandle, struct v4l2_buffer *buf_prt, int index)
{
    // q up the buffer again in order for easy restart
    if (ioctl(*cameraHandle, VIDIOC_QBUF, &buf_prt[index]) < 0)
    {
        printf("VIDIOC_QBUF failed!\n");
        return -1;
    }
    return 0;
}

int main()
{
    float imagesum = 0;
    int imagetimes = 0;
    float lasersum = 0;
    int lasertimes = 0;
    Time result;
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

    int numThreads = 1;

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
                    float imageavg = imagesum/imagetimes;
                    float laseravg = lasersum/lasertimes;

                    printf("I exit Multi now\nThe avg image time is %f \n", imageavg);
                    printf("The avg laser time is %f \n", laseravg);

                    close(cameraHandle);
                    SDL_DestroyRenderer(g_renderer);
                    SDL_DestroyWindow(g_window);
                    SDL_Quit();
                    munmap(imageMemory[0], bufs[0].length);
                    munmap(imageMemory[0], bufs[1].length);

                    return 0;
                }
            }
        }
        SDL_LockTexture(g_streamTexture, NULL, &pixels, &pitch);

        deque(&cameraHandle, bufs, idx);

        result = ProcessImage(imageMemory[bufs[idx].index], bufs[idx].bytesused, pixels,numThreads);

        imagesum += result.image;
        lasersum += result.laser;
        imagetimes += 1;
        lasertimes += 1;


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