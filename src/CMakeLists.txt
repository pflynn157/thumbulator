project(thumbulator)

set(SRC
    decode.c
    except.c
    exmemwb.c
    exmemwb_arith.c
    exmemwb_branch.c
    exmemwb_logic.c
    exmemwb_mem.c
    exmemwb_misc.c
    rsp-server.c
    sim_main.c
    sim_support.c
)

add_executable(thumbulator ${SRC})

target_compile_options(thumbulator PUBLIC -DRAM_START=0x40000000)

target_link_libraries(thumbulator
    ssl
    crypto
)

