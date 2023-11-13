// Anna bergknut, Amanda Björk 1280x720 YUYV
// step 0
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

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

// define the min,max so that it will be easier in yuyv to rgb later
#define MIN(a, b) (((a) < (b)) ? (a) : (b))
#define MAX(a, b) (((a) < (b)) ? (b) : (a))

#define CAM_WIDTH 1280
#define CAM_HEIGHT 720

// the strukt for the pixels
typedef struct Pixel 
{
    unsigned char R;
    unsigned char G;
    unsigned char B;
    unsigned char A;

} Pixel;

// convert yuyv to rgb. y = black and white, u,v = is colour on an xy codinatesystem. 
static void YUYVtoRGB(unsigned char y, unsigned char u, unsigned char v, Pixel* _rgba)
{
    int c = y - 16;
    int d = u - 128;
    int e = v - 128;

    // this is the acutual convertion funktions in order to get rgb from uv.
    _rgba->A = 255; //Alpha
    _rgba->R = MAX(0, MIN((298 * c + 409 * e + 128) >> 8, 255));
    _rgba->G = MAX(0, MIN((298 * c - 100 * d - 208 * e + 128) >> 8, 255));
    _rgba->B = MAX(0, MIN((298 * c + 516 * d + 128) >> 8, 255));
}

// this funktion changes the colour on the choisen pixle
static void Red(Pixel* _rgba)
{
    _rgba->A = 255; //Alpha
    _rgba->R = 255;
    _rgba->G = 0;
    _rgba->B = 0;
}

// for every pixel we check if that pixal is on the cirkle and if yes we send it to red
int DrawCircle(Pixel arrayPicture[], int size, int width, int height)
{
    
    for (int j; j < size; j+=1)
    {
        float val = sqrt( pow(j%width - (width/2), 2) + pow(floor(j/width) -(height/2), 2) );
        if ((100 <= val) && (105 >= val))
        {
            Red(&arrayPicture[j]);
        }
    }
}

// this funktion prosess the image so that it wil be on rgb and call on the funktion to draw the circle. 
int ProcessImage(const unsigned char *_yuv, int _size)
{
    #define RGB_SIZE CAM_WIDTH * CAM_HEIGHT         //1280x720

    static Pixel rgbConversion[RGB_SIZE];
    int rgbIndex = 0;

    // prosses every byte in yuyv
    for (int i = 0; i < _size; i += 4)
    {
        unsigned char y1 = _yuv[i + 0];
        unsigned char u = _yuv[i + 1];
        unsigned char y2 = _yuv[i + 2];
        unsigned char v = _yuv[i + 3];

        YUYVtoRGB(y1, u, v, &rgbConversion[rgbIndex++]);
        YUYVtoRGB(y2, u, v, &rgbConversion[rgbIndex++]);
    }

    DrawCircle(rgbConversion, RGB_SIZE, CAM_WIDTH, CAM_HEIGHT);
    // save the prosessed image
    stbi_write_png("labimage.png",CAM_WIDTH, CAM_HEIGHT, 4, rgbConversion, 5120); 
}

int main()
{
    // variblels
    unsigned char* imageMemory[2];                          // the array that wil store the pixels.
    // step 1
    int cameraHandle = open("/dev/video0", O_RDWR, 0);      // find the camera

    // step 2
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

    // step 3
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

    // forloop in orther to run it twice inother to get 2 buffers.
    int i;
    for (i = 0; i < 2; i++)
    {
        //step 4
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
        
        // step 5
        // create a private mapping into the driver memerory for imagememeroy 
        // this means that later on when we dq the buffer the imagedata will be placed in imagememery
        imageMemory[i] = mmap(NULL, buf.length, PROT_READ, MAP_SHARED, cameraHandle, buf.m.offset);
        
        if(ioctl(cameraHandle, VIDIOC_QBUF, &buf) < 0)
        {
            printf("VIDIOC_QBUF failed!\n");
            return -1;
        }
    }

    // steg 7
    // starts the camera and and q the bufin oder to fill with imagedata
    // type starts
    enum v4l2_buf_type type = V4L2_BUF_TYPE_VIDEO_CAPTURE;

    if (ioctl(cameraHandle, VIDIOC_STREAMON, &type) < 0)
    {
        printf("VIDIOC_STREAMON failed!\n");
        return -1;
    }

    //step 8
    // dq the buffer or stop the new imagedata. this is where step 5 take effect.
    struct v4l2_buffer buf;
    memset(&buf, 0, sizeof(buf));
    buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    buf.memory = V4L2_MEMORY_MMAP;

    if (ioctl(cameraHandle, VIDIOC_DQBUF, &buf) < 0) 
    {
        return errno;
    }

    ProcessImage(imageMemory[buf.index], buf.bytesused);

    // step 9
    // q up the buffer again in order for easy restart
    if (ioctl(cameraHandle, VIDIOC_QBUF, &buf) < 0)
    {
        printf("VIDIOC_QBUF failed!\n");
        return -1;
    }

    close(cameraHandle);

    return 0;
}