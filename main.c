#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>
#include "mpi.h"

struct imageMetadata
{
    int width;
    int height;
    int imageSize;
    char name[512]; // Filename without the extesion TODO: hacer handling en python para que el nombre no supere esos caracteres
};

void blur(unsigned short kernelSize, struct imageMetadata imageData)
{

    char grayscaleFilename[522];
    strcpy(grayscaleFilename, imageData.name);
    strcat(grayscaleFilename, "_gray.bmp");
    FILE *originalImage = fopen(grayscaleFilename, "rb");

    int nameLength = strlen(imageData.name);
    char sufix[20];
    sprintf(sufix, "_blurred_%d.bmp", kernelSize);
    char outputFilename[532];
    strcpy(outputFilename, imageData.name);
    strcat(outputFilename, sufix);
    FILE *outputImage = fopen(outputFilename, "wb");

    unsigned char header[54];
    fread(header, sizeof(unsigned char), 54, originalImage);
    fwrite(header, sizeof(unsigned char), 54, outputImage);

    // Extract pixel array so we can manipulate it and then write it to the output image
    unsigned char *pixelData = (unsigned char *)malloc(imageData.imageSize);
    fread(pixelData, imageData.imageSize, 1, originalImage);

    int kernelRadius = (kernelSize - 1) / 2;

    int widthWithPadding = (imageData.width * 3 + 3) & -4;

    for (int y = 0; y < imageData.height; y++)
    {
        for (int x = 0; x < imageData.width; x++)
        {
            unsigned int rSum = 0;
            unsigned int gSum = 0;
            unsigned int bSum = 0;

            int pond = 0;

            for (int ky = -kernelRadius; ky <= kernelRadius; ky++)
            {
                for (int kx = -kernelRadius; kx <= kernelRadius; kx++)
                {
                    // Kernel sliding along the pixel at (x,y)
                    int i = y + ky;
                    int j = x + kx;

                    // Check if the kernel cordinate (i,j) is within image boundries
                    // If it isn't, we just don't consider it for the (x,y) pixel's wighted sum
                    if (i < 0 || i >= imageData.height || j < 0 || j >= imageData.width)
                        continue;

                    // Each row of pixels contains its corresponding padding, so we need
                    // to use the width accounting for padding instead of just the width
                    int index = (i * widthWithPadding) + (j * 3);
                    bSum += pixelData[index];
                    gSum += pixelData[index + 1];
                    rSum += pixelData[index + 2];
                    pond++;
                }
            }

            unsigned char bAvg = bSum / pond;
            unsigned char gAvg = gSum / pond;
            unsigned char rAvg = rSum / pond;

            int index = (y * widthWithPadding) + (x * 3);
            pixelData[index] = bAvg;
            pixelData[index + 1] = gAvg;
            pixelData[index + 2] = rAvg;
        }
    }

    fwrite(pixelData, imageData.imageSize, 1, outputImage);
    fclose(outputImage);
    fclose(originalImage);

    free(pixelData);
    free(sufix);
}

int main(int argc, char *argv[])
{
    MPI_Init(&argc, &argv);

    int rank, nprocs, len;
    char name[MPI_MAX_PROCESSOR_NAME];
    MPI_Get_processor_name(name, &len);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);

    char *filename = NULL;
    int initialMask = 11;
    struct imageMetadata imageData;

    if (rank == 0)
    {

        // Qué debe de tener config:
        // * nprocs -> número de máscaras a generar (se especiica en la GUI y se lee desde la command line al correr el programa)*/
        for (int i = 1; i < argc; i++)
        {
            if (strcmp(argv[i], "-f") == 0 && i + 1 < argc)
                filename = argv[i + 1];

            if (strcmp(argv[i], "-m") == 0 && i + 1 < argc)
            {
                if (isdigit(argv[i + 1][0]))
                    initialMask = atoi(argv[i + 1]);
            }
        }

        FILE *originalImage = fopen(filename, "rb");
        strtok(filename, ".");
        unsigned char header[54];
        fread(header, sizeof(unsigned char), 54, originalImage);

        int width = *(int *)&header[18];
        int height = *(int *)&header[22];
        int imageSize = *(int *)&header[34];
        imageData.height = height;
        imageData.width = width;
        imageData.imageSize = imageSize;
        strcpy(imageData.name, filename);
        char *outputFilename = malloc(10 + strlen(filename));
        strcpy(outputFilename, filename);
        FILE *outputImage = fopen(strcat(outputFilename, "_gray.bmp"), "wb");
        fwrite(header, sizeof(unsigned char), 54, outputImage);

        int widthWithPadding = (width * 3 + 3) & -4;
        int padding = widthWithPadding - (width * 3);

        unsigned char pixel[3];
        unsigned char paddingPixels[widthWithPadding];

        for (int y = 0; y < height; y++)
        {
            for (int x = 0; x < width; x++)
            {
                fread(pixel, 3, 1, originalImage);
                unsigned char gray = pixel[0] * 0.07 + pixel[1] * 0.72 + pixel[2] * 0.21;
                memset(pixel, gray, sizeof(pixel));
                fwrite(&pixel, 3, 1, outputImage);
            }
            fread(paddingPixels, padding, 1, originalImage);
            fwrite(paddingPixels, padding, 1, outputImage);
        }

        fclose(outputImage);
        fclose(originalImage);

        free(outputFilename);
    }

    MPI_Barrier(MPI_COMM_WORLD);

    MPI_Bcast(&imageData, sizeof(struct imageMetadata), MPI_BYTE, 0, MPI_COMM_WORLD);

    if (rank < nprocs && (rank + 1) % 2 != 0)
    {
        int n = nprocs - rank + initialMask;
        blur(n, imageData);
    }

    MPI_Finalize();

    return 0;
}

