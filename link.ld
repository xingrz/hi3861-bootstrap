OUTPUT_ARCH( "riscv" )
ENTRY(_start)

MEMORY
{
    /* CPU_RAM */
    HEAP(xrw):              ORIGIN = 0x000D8000+16K,        LENGTH = 144K
    STACK(xrw) :            ORIGIN = 0x000D8000+160K,       LENGTH = 8K
    ROM_BSS_DATA(rx):       ORIGIN = 0x000D8000+176K,       LENGTH = 2K
    CODE_ROM_BSS_DATA(rx):  ORIGIN = 0x000D8000+178K,       LENGTH = 2K
    FLASH_BOOT(rwx) :       ORIGIN = 0x000D8000+200K+0x040, LENGTH = 32K-0x040-0x3C0
    /* ROM */
    CODE_ROM(rx):           ORIGIN = 0x003B8000+278K,       LENGTH = 10K
}

SECTIONS
{
      /* The startup code goes first into FLASH */
    .text.entry : ALIGN(4)
    {
        KEEP(*(.text.entry))
    } > FLASH_BOOT

    .rom.code.text :
    {
        . = ALIGN(4);
        KEEP(SORT(libcodebase.o)(.text*))
        KEEP(SORT(libcodebase.o)(.rodata*))
        . = ALIGN(4);
    } > CODE_ROM

    /* Stack in SRAM at Highest addresses */
    .stacks (NOLOAD) :
    {
        . = ALIGN(4);
        __SYSTEM_STACK_BEGIN__ = ORIGIN(STACK);
        KEEP(*(.stacks))
        __SYSTEM_STACK_END__ = ORIGIN(STACK) + LENGTH(STACK);
    } > STACK
    __SYSTEM_STACK_SIZE__ = __SYSTEM_STACK_END__ - __SYSTEM_STACK_BEGIN__;
    __stack_top = __SYSTEM_STACK_END__;

    .rom.data :
    {
        . = ALIGN(4);
        __rom_copy_start = LOADADDR(.rom.data);
        . = ALIGN(4);
        __rom_copy_ram_start = .;
        __global_pointer$ = .;
        KEEP(SORT(libbase.o) (.data*))
        . = ALIGN(4);
        __rom_copy_ram_end = .;
    } > ROM_BSS_DATA
    __rom_copy_size = __rom_copy_ram_end - __rom_copy_ram_start;

    .rom.code.data :
    {
        . = ALIGN(4);
        __code_rom_copy_start = LOADADDR(.rom.code.data);
        . = ALIGN(4);
        __code_rom_copy_ram_start = .;
        KEEP(SORT(libcodebase.o) (.data*))
        . = ALIGN(4);
        __code_rom_copy_ram_end = .;
    } > CODE_ROM_BSS_DATA AT>CODE_ROM
    __code_rom_copy_size = __code_rom_copy_ram_end - __code_rom_copy_ram_start;

    .rom.bss :
    {
        . = ALIGN(4);
        __rom_bss_start = .;
        KEEP(libbase.o (.bss))
        KEEP(libbase.o (.bss*))
        KEEP(libbase.o (COMMON))
        . = ALIGN(4);
        __rom_bss_end = .;
    } > ROM_BSS_DATA

    .rom.code.bss :
    {
        . = ALIGN(4);
        __code_rom_bss_start = .;
        KEEP(libcodebase.o (.bss))
        KEEP(libcodebase.o (.bss*))
        KEEP(libcodebase.o (COMMON))
        . = ALIGN(4);
        __code_rom_bss_end = .;
    } > CODE_ROM_BSS_DATA AT>CODE_ROM

    .text : ALIGN(4)
    {
        __start_addr = .;
        *(.text*)
        . = ALIGN(4);
        __rodata_start = .;
        *(.rodata*)
        . = ALIGN(4);
        __rodata_end = .;
        __text_end = .;
    } > FLASH_BOOT

    /* data section */
    .data : ALIGN(4)
    {
        __data_load = LOADADDR(.data);
        __data_start = .;
        *(.data*)
        . = ALIGN(4);
        __data_end = .;
    } > FLASH_BOOT

    /* bss section */
    .bss (NOLOAD) : ALIGN(4)
    {
        __bss_begin__ = .;
        *(.bss*)
        *(COMMON)
        . = ALIGN(4);
        __bss_end__ = .;
    } > FLASH_BOOT
    __bss_size__ = __bss_end__ - __bss_begin__;

    .heap (NOLOAD) :
    {
        . = ALIGN(4);
        __heap_begin__ = ORIGIN(HEAP);
        KEEP(*(.heap))
        __heap_end__ =  __heap_begin__ + LENGTH(HEAP);
    } > HEAP
}
