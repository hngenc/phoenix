#include <iostream>
#include <string>
#include <vector>
#include <sl/Camera.hpp>
#include <string>

using namespace std;
using namespace sl;


int main(int argc, char **argv)
{
    // Create a ZED camera object
    Camera zed;

    // Vector values to store
    vector<float> depth_vals;
    vector<float> left_vals;
    vector<float> right_vals;

    // Set configuration parameters
    InitParameters init_params;
    init_params.depth_mode = DEPTH_MODE_PERFORMANCE; // Use PERFORMANCE depth mode
    init_params.coordinate_units = UNIT_METER; // Use millimeter units (for depth measurements)

    // Open the camera
    ERROR_CODE err = zed.open(init_params);
    if (err != SUCCESS)
        exit(-1);

    // Set runtime parameters after opening the camera
    RuntimeParameters runtime_parameters;
    runtime_parameters.sensing_mode = SENSING_MODE_STANDARD; // Use STANDARD sensing mode

    // Capture 50 images and depth, then stop
    int samples = stoi(string(argv[1]));
    int i = 0;
    sl::Mat left, right, depth;

    while (i  < samples) {
        // A new image is available if grab() returns SUCCESS
        if (zed.grab(runtime_parameters) == SUCCESS) {
            // Retrieve left image
            zed.retrieveImage(left, VIEW_LEFT);
            // Retrieve right image
            zed.retrieveImage(right, VIEW_RIGHT);
            // Retrieve depth map. Depth is aligned on the left image
            zed.retrieveMeasure(depth, MEASURE_DEPTH);

            // Get and print distance value in mm at the center of the image
            // We measure the distance camera - object using Euclidean distance
            int x = left.getWidth() / 2;
            int y = left.getHeight() / 2;

            // Read center values
            float f;
            depth.getValue(x, y, &f);
            depth_vals.push_back(f);

            // right.getValue(x, y, &f);
            // right_vals.push_back(f);

            // left.getValue(x, y, &f);
            // left_vals.push_back(f);

      		// Increment the loop
            i++;
        }
    }

    // Close the camera
    zed.close();

    for (int i = 0; i < samples; i++) {
        cout << depth_vals[i] << endl;
        // cout << right_vals[i] << endl;
        // cout << left_vals[i] << endl;
    }

    return 0;
}


