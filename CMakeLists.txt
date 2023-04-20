cmake_minimum_required(VERSION 3.20)

set(CMAKE_EXPORT_COMPILE_COMMANDS 1)

set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(CMAKE_C_COMPILER_FORCED 1)
set(CMAKE_CXX_COMPILER_FORCED 1)

set(RISCV32_TOOLCHAIN_PATH "$ENV{RISCV32_TOOLCHAIN_PATH}")
if(NOT RISCV32_TOOLCHAIN_PATH)
    message(FATAL_ERROR "RISCV32_TOOLCHAIN_PATH is not set")
endif()

set(TOOLCHAIN_HOME ${RISCV32_TOOLCHAIN_PATH})

set(CROSS_COMPILE_TARGET riscv32-unknown-elf)
set(CROSS_COMPILE ${TOOLCHAIN_HOME}/bin/${CROSS_COMPILE_TARGET}-)

set(CMAKE_C_COMPILER ${CROSS_COMPILE}gcc)
set(CMAKE_CXX_COMPILER ${CROSS_COMPILE}g++)
set(CMAKE_LINKER ${CROSS_COMPILE}ld)
set(CMAKE_OBJCOPY ${CROSS_COMPILE}objcopy)
set(CMAKE_SIZE ${CROSS_COMPILE}size)

project(hi3861 C ASM)

add_executable(app)
set(CMAKE_EXECUTABLE_SUFFIX .elf)

target_sources(app PRIVATE src/riscv_init.S)
target_sources(app PRIVATE src/main.c)
target_sources(app PRIVATE src/stack_protect.c)

target_include_directories(app PRIVATE include)

target_compile_options(app PRIVATE
    -mabi=ilp32 -march=rv32imc -freorder-blocks-algorithm=simple
    -fno-schedule-insns -nostdinc -fno-aggressive-loop-optimizations
    -fno-builtin -fno-exceptions -fno-short-enums -mtune=size
    -msmall-data-limit=0 -Wall -Werror -Os -std=c99 -falign-functions=2
    -fdata-sections -ffunction-sections -fno-common -fstack-protector-strong
)

target_link_options(app PRIVATE
    -nostdlib -nostartfiles
)

target_link_options(app PRIVATE -L${CMAKE_CURRENT_SOURCE_DIR}/libs)
target_link_options(app PRIVATE -T${CMAKE_CURRENT_SOURCE_DIR}/link.ld)

add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/app.bin
    COMMAND ${CMAKE_OBJCOPY} -O binary
            ${CMAKE_CURRENT_BINARY_DIR}/app.elf
            ${CMAKE_CURRENT_BINARY_DIR}/app.bin
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/app.elf
)

add_custom_target(
    build ALL
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/app.bin
)
