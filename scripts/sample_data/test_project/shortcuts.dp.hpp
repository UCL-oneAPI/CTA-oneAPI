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
        /*
DPCT1003:29: Migrated API does not return error code. (*, 0) is inserted. You
may need to rewrite this code.
*/
        /*
DPCT1003:209: Migrated API does not return error code. (*, 0) is inserted. You
may need to rewrite this code.
*/
        DEBUG_HANDLE_ERROR((dpct::get_default_queue()
                                .memcpy(d_ptr, h_ptr, size * sizeof(T))
                                .wait(),
                            0));
};

template <typename T>
static inline void cpyHostToDevice(T *h_ptr, T *d_ptr, size_t size,
                                   sycl::queue *stream)
{
        /*
DPCT1003:30: Migrated API does not return error code. (*, 0) is inserted. You
may need to rewrite this code.
*/
        /*
DPCT1003:210: Migrated API does not return error code. (*, 0) is inserted. You
may need to rewrite this code.
*/
        DEBUG_HANDLE_ERROR((stream->memcpy(d_ptr, h_ptr, size * sizeof(T)), 0));
};

template< typename T>
static inline
void cpyDeviceToHost( T *d_ptr, T *h_ptr, size_t size)
{
        /*
DPCT1003:31: Migrated API does not return error code. (*, 0) is inserted. You
may need to rewrite this code.
*/
        /*
DPCT1003:211: Migrated API does not return error code. (*, 0) is inserted. You
may need to rewrite this code.
*/
        DEBUG_HANDLE_ERROR((dpct::get_default_queue()
                                .memcpy(h_ptr, d_ptr, size * sizeof(T))
                                .wait(),
                            0));
};

template <typename T>
static inline void cpyDeviceToHost(T *d_ptr, T *h_ptr, size_t size,
                                   sycl::queue *&stream)
{
        /*
DPCT1003:32: Migrated API does not return error code. (*, 0) is inserted. You
may need to rewrite this code.
*/
        /*
DPCT1003:212: Migrated API does not return error code. (*, 0) is inserted. You
may need to rewrite this code.
*/
        DEBUG_HANDLE_ERROR((stream->memcpy(h_ptr, d_ptr, size * sizeof(T)), 0));
};

template <typename T>
static inline void cpyDeviceToDevice(T *src, T *des, size_t size,
                                     sycl::queue *&stream)
{
        /*
DPCT1003:33: Migrated API does not return error code. (*, 0) is inserted. You
may need to rewrite this code.
*/
        /*
DPCT1003:213: Migrated API does not return error code. (*, 0) is inserted. You
may need to rewrite this code.
*/
        DEBUG_HANDLE_ERROR((stream->memcpy(des, src, size * sizeof(T)), 0));
};

template< typename T>
static inline
void memInit( T *ptr, T value, size_t size)
{
        /*
DPCT1003:34: Migrated API does not return error code. (*, 0) is inserted. You
may need to rewrite this code.
*/
        /*
DPCT1003:214: Migrated API does not return error code. (*, 0) is inserted. You
may need to rewrite this code.
*/
        DEBUG_HANDLE_ERROR((dpct::get_default_queue()
                                .memset(ptr, value, size * sizeof(T))
                                .wait(),
                            0));
};

template <typename T>
static inline void memInit(T *ptr, T value, size_t size, sycl::queue *&stream)
{
        /*
DPCT1003:35: Migrated API does not return error code. (*, 0) is inserted. You
may need to rewrite this code.
*/
        /*
DPCT1003:215: Migrated API does not return error code. (*, 0) is inserted. You
may need to rewrite this code.
*/
        DEBUG_HANDLE_ERROR((stream->memset(ptr, value, size * sizeof(T)), 0));
};

}
#endif //CUDA_SHORTCUTS_CUH_
