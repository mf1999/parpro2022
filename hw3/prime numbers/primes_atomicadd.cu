#include <iostream>


__global__ void check(int n, int* deviceCount) {
    int index = blockIdx.x * blockDim.x + threadIdx.x; // which block (1,2,3...) * block 'width' (32,64,...) + thread offset(1,2,3...)
    int stride = blockDim.x * gridDim.x; // block 'width' (32,64,...) * number of blocks
    for (int i = index; i < n; i += stride) {
        bool isPrime = true;
        for (int j = 2; j < (i + 1); j++) {
            if (((i + 1) % j) == 0) { 
                isPrime = false; 
            }
        } 
        if (isPrime) {
            atomicAdd(deviceCount, 1);
        }
    }
}


int main() {
    int N = pow(2, 15);

    int* d_data, * h_data;

    h_data = (int*)malloc(1 * sizeof(int));
    cudaMalloc((void**)&d_data, 1 * sizeof(int));

    cudaMemset(d_data, 0, 1 * sizeof(int));

    int blockSize = 32; // number of threads per block
    int numBlocks = (N + blockSize - 1) / blockSize; // optimally we need (N / blockSize) blocks, rounded up
    check << <numBlocks, blockSize >> > (N, d_data);
    //check << <1, 1 >> > (N, d_data);
    cudaDeviceSynchronize();

    cudaMemcpy(h_data, d_data, 1 * sizeof(int), cudaMemcpyDeviceToHost);
    printf("First %d numbers have %d primes.\n", N, *h_data);
    return 0;
}