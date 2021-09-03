#include <CL/sycl.hpp>
#include <dpct/dpct.hpp>
#ifndef CUDA_SHORTCUTS_CUH_
#define CUDA_SHORTCUTS_CUH_

namespace CudaShortcuts
{

/**
 * Print cuda device memory info
 */
static void printMemInfo()
{
	size_t free;
	size_t total;
	DEBUG_HANDLE_ERROR(cudaMemGetInfo( &free, &total ));
	float free_hr(free/(1024.*1024.));
	float total_hr(total/(1024.*1024.));
    printf( "free %.2fMiB, total %.2fMiB, used %.2fMiB\n",
    		free_hr, total_hr, total_hr - free_hr);
}

template< typename T>
static inline
void cpyHostToDevice( T *h_ptr, T *d_ptr, size_t size)
{
        dpct::get_default_queue().memcpy(d_ptr, h_ptr, size * sizeof(T)).wait();
};

template <typename T>
static inline void cpyHostToDevice(T *h_ptr, T *d_ptr, size_t size,
                                   sycl::queue *stream)
{
        stream->memcpy(d_ptr, h_ptr, size * sizeof(T));
};

template< typename T>
static inline
void cpyDeviceToHost( T *d_ptr, T *h_ptr, size_t size)
{
        dpct::get_default_queue().memcpy(h_ptr, d_ptr, size * sizeof(T)).wait();
};

template <typename T>
static inline void cpyDeviceToHost(T *d_ptr, T *h_ptr, size_t size,
                                   sycl::queue *&stream)
{
        stream->memcpy(h_ptr, d_ptr, size * sizeof(T));
};

template <typename T>
static inline void cpyDeviceToDevice(T *src, T *des, size_t size,
                                     sycl::queue *&stream)
{
        stream->memcpy(des, src, size * sizeof(T));
};

template< typename T>
static inline
void memInit( T *ptr, T value, size_t size)
{
        dpct::get_default_queue().memset(ptr, value, size * sizeof(T)).wait();
};

template <typename T>
static inline void memInit(T *ptr, T value, size_t size, sycl::queue *&stream)
{
        stream->memset(ptr, value, size * sizeof(T));
};

}
#endif //CUDA_SHORTCUTS_CUH_
