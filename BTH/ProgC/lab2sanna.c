// Anna bergknut, Amanda Björk 1280x720 YUYV
// step 0 lab1
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
#include <math.h>               // calculate the ring

#include <SDL2/SDL.h>           // step 0 lab2
#include <omp.h>                // steg 3 lab2

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

// define the min,max so that it will be easier in yuyv to rgb later
#define MIN(a, b) (((a) < (b)) ? (a) : (b))
#define MAX(a, b) (((a) < (b)) ? (b) : (a))

#define CAM_WIDTH 640
#define CAM_HEIGHT 360

// the strukt for the pixels
typedef struct Pixel 
{
    unsigned char R;
    unsigned char G;
    unsigned char B;
    unsigned char A;
} Pixel;

// convert yuyv to rgb. y = black and white, u,v = is colour on an xy codinatesystem. 
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
    
    if(blue>=230 && green>=230 && red>=230)
    {
       return 1;
    } 
    return 0;
}

// this funktion changes the colour on the choisen pixle
static void Red(Pixel* _rgba)
{
    _rgba->A = 255; //Alpha
    _rgba->R = 255;
    _rgba->G = 0;
    _rgba->B = 0;
}

int coordinates ( int xVal, int yVal)
{
    if( yVal <= (CAM_HEIGHT/3))
    {
        printf("Back \n");
    }
    else if( xVal <= (CAM_WIDTH/4))
    {
        printf("Left \n");
    }
    else if(xVal >= (CAM_WIDTH-(CAM_WIDTH/4)))
    {
        printf("Right \n");
    }
    else
    {
        printf("Forward \n");
    }
    return 0;
}

// this funktion prosess the image so that it wil be on rgb and call on the funktion to draw the circle. 
int ProcessImage(const unsigned char *_yuv, int _size, void *pixels)
{
    #define RGB_SIZE CAM_WIDTH * CAM_HEIGHT
    // static Pixel rgbConversion[RGB_SIZE];
    Pixel* rgbConversion = (Pixel*)pixels;
    int found = 0;
    
    int rgbIndex = 0;
    // printf("%d \n", _size);

    // prosses every byte in yuyv
    for (int i = 0; i < _size; i += 4)
    {
        unsigned char y1 = _yuv[i + 0];
        unsigned char u = _yuv[i + 1];
        unsigned char y2 = _yuv[i + 2];
        unsigned char v = _yuv[i + 3];

        if (YUYVtoRGB(y1, u, v, &rgbConversion[rgbIndex++])== 1 && found == 0)
        {
            found = 1;
        }
        if(YUYVtoRGB(y2, u, v, &rgbConversion[rgbIndex++]) == 1 && found == 0)
        {
            found = 1;
        }
        if (found == 1)
        {
            int j = i/2;
            printf("found \n");
            int xVal = j%CAM_WIDTH;
            int yVal = floor(j/CAM_WIDTH);
            printf("coordinates are %d and %d \n", xVal, yVal);
            coordinates ( xVal, yVal);
            found = 2;
        }
    }
    
}

int bufMap(int cameraHandle, unsigned char** imageMemory)
{
    // forloop in orther to run it twice inother to get 2 buffers.
    int i;
    for (i = 0; i < 2; i++)
    {
        //step 4 lab1
        // create the buffer and sets the memeroy to 0 and decler typ and size. 
        struct v4l2_buffer buf;
        memset(&buf, 0, sizeof(buf));
        buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE; // we tell what the type will do. will make use of this in step 7
        buf.memory = V4L2_MEMORY_MMAP;
        buf.index = i;

        if (ioctl(cameraHandle, VIDIOC_QUERYBUF, &buf) < 0)
        {
            printf("VIDIOC_QUERYBUF failed!\n");
            return -1;
        }
        
        // step 5 lab1
        // create a private mapping into the driver memerory for imagememeroy 
        // this means that later on when we dq the buffer the imagedata will be placed in imagememery
        imageMemory[i] = mmap(NULL, buf.length, PROT_READ, MAP_SHARED, cameraHandle, buf.m.offset);
        
        if(ioctl(cameraHandle, VIDIOC_QBUF, &buf) < 0)
        {
            printf("VIDIOC_QBUF failed!\n");
            return -1;
        }
    }
}

int startCamera(int cameraHandle)
{
    // steg 7 lab1
    // starts the camera and and q the bufin oder to fill with imagedata
    // type starts
    enum v4l2_buf_type type = V4L2_BUF_TYPE_VIDEO_CAPTURE;

    if (ioctl(cameraHandle, VIDIOC_STREAMON, &type) < 0)
    {
        printf("VIDIOC_STREAMON failed!\n");
        return -1;
    }
}
    
int allocateMemory(int cameraHandle)
{
    // step 3 lab1
    // allocate the memery needed for the image data and create the mapping
    struct v4l2_requestbuffers req;
    memset(&req, 0, sizeof(req));
    req.count = 2;
    req.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    req.memory = V4L2_MEMORY_MMAP;

    if (ioctl(cameraHandle, VIDIOC_REQBUFS, &req) < 0)
    {
        printf("VIDIOC_REQBUFS failed!\n");
        return -1;
    }
}

int main()
{
    // variblels
    unsigned char* imageMemory[2];                          // the array that wil store the pixels.
    // step 1 lab1
    int cameraHandle = open("/dev/video0", O_RDWR, 0);      // find the camera

    // step 2 lab1
    // declearade the formate that we will use for the camera. such as the pixels and dimantions of the camera.
    struct v4l2_format format;
    memset(&format,0,sizeof(format));
    format.type = V4L2_BUF_TYPE_VIDEO_CAPTURE; 
    format.fmt.pix.width = CAM_WIDTH; 
    format.fmt.pix.height =CAM_HEIGHT; 
    format.fmt.pix.pixelformat = V4L2_PIX_FMT_YUYV;
    format.fmt.pix.field = V4L2_FIELD_ANY;

    if (ioctl(cameraHandle, VIDIOC_S_FMT, &format) < 0)
    {
        printf("VIDIOC_S_FMT Video format set fail\n");
        return -1;
    }
    
    // step 1 lab2
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window *g_window = SDL_CreateWindow("SDL Window", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, CAM_WIDTH, CAM_HEIGHT, SDL_WINDOW_OPENGL | SDL_WINDOW_SHOWN);
    SDL_Renderer *g_renderer = SDL_CreateRenderer(g_window, -1, SDL_RENDERER_ACCELERATED);
    SDL_Texture *g_streamTexture = SDL_CreateTexture(g_renderer, SDL_PIXELFORMAT_ARGB8888, SDL_TEXTUREACCESS_STREAMING, CAM_WIDTH, CAM_HEIGHT);

    void *pixels;

    int pitch;

    allocateMemory(cameraHandle);
    
    bufMap(cameraHandle,imageMemory);
    
    startCamera(cameraHandle);

    //step 8 lab1
    // dq the buffer or stop the new imagedata. this is where step 5 take effect.
    struct v4l2_buffer buf;
    memset(&buf, 0, sizeof(buf));
    buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    buf.memory = V4L2_MEMORY_MMAP;

    SDL_Event event;

    while (1)
    {
        if (SDL_PollEvent(&event))
        {
            if (event.type == SDL_KEYDOWN)
            {
                if (event.key.keysym.sym == SDLK_ESCAPE)
                {
                    printf("I exit now single: \n");

                    close(cameraHandle);

                    // step 1 lab2
                    SDL_DestroyRenderer(g_renderer);
                    SDL_DestroyWindow(g_window);
                    SDL_Quit();

                    return 0;
                }
            }
        }
        
        double t0 = omp_get_wtime();

        SDL_LockTexture(g_streamTexture, NULL, &pixels, &pitch);

        if (ioctl(cameraHandle, VIDIOC_DQBUF, &buf) < 0) 
        {
            return errno;
        }

        ProcessImage(imageMemory[buf.index], buf.bytesused, pixels);
        printf("new frame\n");

        // step 9 lab1
        // q up the buffer again in order for easy restart
        if (ioctl(cameraHandle, VIDIOC_QBUF, &buf) < 0)
        {
            printf("VIDIOC_QBUF failed!\n");
            return -1;
        }

        SDL_UnlockTexture(g_streamTexture);

        SDL_RenderCopy(g_renderer, g_streamTexture, NULL, NULL);

        SDL_RenderPresent(g_renderer);

        double milliseconds = (omp_get_wtime() - t0) * 1000;

        printf("Time spent: %5.2fms\r", milliseconds);
    
    }

    return 0;
}