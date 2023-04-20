#include "hi_boot_rom.h"

HI_EXTERN hi_u32 __heap_begin__;
HI_EXTERN hi_u32 __heap_end__;

hi_void
app_main(hi_void)
{
	hi_watchdog_disable();

	hi_io_set_func(HI_IO_NAME_GPIO_3, HI_IO_FUNC_GPIO_3_UART0_TXD); /* uart0 tx */
	hi_io_set_func(HI_IO_NAME_GPIO_4, HI_IO_FUNC_GPIO_4_UART0_RXD); /* uart0 rx */

	hi_malloc_func malloc_funcs;
	malloc_funcs.init = rom_boot_malloc_init;
	malloc_funcs.boot_malloc = rom_boot_malloc;
	malloc_funcs.boot_free = rom_boot_free;
	hi_register_malloc((uintptr_t)&__heap_begin__, &malloc_funcs);
	hi_u32 check_sum = ((uintptr_t)&__heap_begin__) ^ ((uintptr_t)&__heap_end__);
	boot_malloc_init((uintptr_t)&__heap_begin__, (uintptr_t)&__heap_end__, check_sum);

	uart_param_stru default_uart_param = {
		.baudrate = 115200,
		.databit = 8,
		.stopbit = 1,
		.parity = 0,
		.flow_ctrl = 0,
		.fifoline_tx_int = 0,
		.fifoline_rx_int = 2,
		.fifoline_rts = 1,
		.pad = 4,
	};
	serial_init(UART0, default_uart_param);

	boot_msg0("Hello world!");

	for (int i = 0;; i++) {
		boot_msg1("i = ", i);
		mdelay(1000);
	}
}
