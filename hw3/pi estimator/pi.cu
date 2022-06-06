#include <math.h>
#include <stdio.h>
__global__
void do_sum(int n, double* sum)
{
	int index = blockIdx.x * blockDim.x + threadIdx.x;
	int stride = blockDim.x * gridDim.x;

	double x;
	double sum_spec;
	
	for (int i = index + 1; i < n; i += stride) {
		x = (float)(i - 0.5) / n;
		sum_spec = (float) 1 / (1 + (x*x));
		atomicAdd(sum, sum_spec);
	}

}
int main(int argc, char* argv[])
{
	double PI25DT = 3.141592653589793238462643;

	int N;
	printf("Enter the number of intervals: (0 quits) ");
	scanf("%d", &N);
	if (N == 0) return 0;
	
	double* sum;
	int blockSize = 32 * 1;
	int numBlocks = (N + blockSize - 1) / blockSize;

	cudaMallocManaged(&sum, sizeof(double));
	cudaMemset(sum, 0, sizeof(double));

	do_sum << <numBlocks, blockSize >> > (N, sum);

	cudaDeviceSynchronize();

	double* pi = (double*)malloc(sizeof(double));
	cudaMemcpy(pi, sum, sizeof(double), cudaMemcpyDeviceToHost);
	cudaFree(sum);

	*pi = *pi * 4 / N;
	printf("Pi is approximately %.16f, Error is %.16f\n", *pi, fabs(*pi - PI25DT));

	return 0;
	
}