#include "hi_boot_rom.h"

hi_void
app_main(hi_void)
{
	hi_watchdog_disable();

	hi_io_set_func(HI_IO_NAME_GPIO_3, HI_IO_FUNC_GPIO_3_UART0_TXD); /* uart0 tx */
	hi_io_set_func(HI_IO_NAME_GPIO_4, HI_IO_FUNC_GPIO_4_UART0_RXD); /* uart0 rx */

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
