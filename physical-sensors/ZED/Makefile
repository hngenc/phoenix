all:
	g++ monitor.cpp -std=c++11 -o monitor -I /usr/local/zed/include/ -I /usr/local/cuda/include/ -L /usr/local/zed/lib/ -lsl_calibration -lsl_disparityFusion -lsl_tracking -lsl_core -lsl_scanning -lsl_zed

run:
	./monitor
