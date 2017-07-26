#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>

using namespace cv;
using namespace std;

/**
Function that returns the maximum of 3 integers
@param a first integer
@param b second integer
@param c third integer
*/
int myMax(int a, int b, int c);

/**
Function that returns the minimum of 3 integers
@param a first integer
@param b second integer
@param c third integer
*/
int myMin(int a, int b, int c);

/**
Function that detects whether a pixel belongs to the skin based on RGB values
@param src The source color image
@param dst The destination grayscale image where skin pixels are colored white and the rest are colored black
*/
void mySkinDetect(Mat& src, Mat& dst);

/** @function main */
int main(int argc, char** argv)
{
	//----------------
	//a) Reading a stream of images from a webcamera, and displaying the video
	//----------------
	// For more information on reading and writing video: http://docs.opencv.org/modules/highgui/doc/reading_and_writing_images_and_video.html
	// open the video camera no. 0
	VideoCapture cap(0);

	// if not successful, exit program
	if (!cap.isOpened())
	{
		cout << "Cannot open the video cam" << endl;
		return -1;
	}

	//create a window called "MyVideoFrame0"
	// namedWindow("MyVideo0", WINDOW_AUTOSIZE);
	namedWindow("Source", WINDOW_AUTOSIZE);
	namedWindow("MyVideo", WINDOW_AUTOSIZE);
	Mat frame0;

	// read a new frame from video
	bool bSuccess0 = cap.read(frame0);

	//if not successful, break loop
	if (!bSuccess0)
	{
		cout << "Cannot read a frame from video stream" << endl;
	}

	
	while (1)
	{
		// read a new frame from video
		Mat frame;
		bool bSuccess = cap.read(frame);

		//if not successful, break loop
		if (!bSuccess)
		{
			cout << "Cannot read a frame from video stream" << endl;
			break;
		}

		// destination frame
		Mat frameDest;
		frameDest = Mat::zeros(frame.rows, frame.cols, CV_8UC1); //Returns a zero array of same size as src mat, and of type CV_8UC1
		
		// Load source image and convert it to gray
		frameDest = Mat::zeros(frame.rows, frame.cols, CV_8UC1);
		mySkinDetect(frame, frameDest);
		Mat src = frameDest.clone();
		
		erode(src,src,Mat());
		dilate(src,src,Mat());
		
		Mat threshold_output;
		vector<vector<Point> > contours;
		vector<Vec4i> hierarchy;

		/// Detect edges using Threshold
		threshold(src, threshold_output, 50, 255, THRESH_BINARY);

		/// Find contours
		findContours(threshold_output, contours, hierarchy, CV_RETR_EXTERNAL, CHAIN_APPROX_SIMPLE, Point(0, 0));
		
		/// hull
		vector<vector<Point> >hull(contours.size());
		
		vector<vector<int> > hullsI(contours.size()); // Indices to contour points
		vector<vector<Vec4i> > defects(contours.size());
		
		for (int i = 0; i < contours.size(); i++)
		{
			convexHull(Mat(contours[i]), hull[i], false);
		}
		
		int largest_contour_index = -1;
		int largest_area = 0;
		
		/// largest contour
		for (int i = 0; i< contours.size(); i++) // iterate through each contour. 
		{
		    double a = contourArea(contours[i], false);  //  Find the area of contour
		    if (a>largest_area){
		        largest_area = a;
		        largest_contour_index = i;                //Store the index of largest contour
		    }

		}
		
		convexHull(contours[largest_contour_index], hull[largest_contour_index], false);
	    convexHull(contours[largest_contour_index], hullsI[largest_contour_index], false); 
        convexityDefects(contours[largest_contour_index], hullsI[largest_contour_index], defects[largest_contour_index]);
		
		String size = "";
		int size_ = 0;
		
		for(int j=0; j<defects[largest_contour_index].size(); ++j)
		{
			const Vec4i& v = defects[largest_contour_index][j];
			float depth = v[3] / 256;
			if (depth > 100) //  filter defects by depth
			{
			    // int startidx = v[0]; Point ptStart(contours[largest_contour_index][startidx]);
			    int endidx = v[1]; Point ptEnd(contours[largest_contour_index][endidx]);
			    // int faridx = v[2]; Point ptFar(contours[largest_contour_index][faridx]);

			    // line(frame, ptStart, ptEnd, Scalar(0, 255, 0), 1);
			    // line(frame, ptStart, ptFar, Scalar(0, 255, 0), 1);
			    // line(frame, ptEnd, ptFar, Scalar(0, 255, 0), 1);
			    circle(frame, ptEnd, 4, Scalar(0, 255, 0), 2);
				size_++;
			}
		}
		size = "Number of fingertips: " + std::to_string(size_);
		Scalar color = Scalar(0, 255, 0);
		// drawContours(frame, contours, largest_contour_index, color, 1, 8, vector<Vec4i>(), 0, Point());
		drawContours(frame, hull, largest_contour_index, color, 1, 8, vector<Vec4i>(), 0, Point());
		
		/// Show in a window
		namedWindow("Hull demo", CV_WINDOW_AUTOSIZE);
		putText(frame, size, cvPoint(60,60), FONT_HERSHEY_SIMPLEX, 2.0, cvScalar(0,0,255), 4, CV_AA);
		imshow("Hull demo", frame);
		
		

		waitKey(30);
		
	}
	cap.release();
	return(0);
}

//Function that returns the maximum of 3 integers
int myMax(int a, int b, int c) {
	int m = a;
	(void)((m < b) && (m = b));
	(void)((m < c) && (m = c));
	return m;
}

//Function that returns the minimum of 3 integers
int myMin(int a, int b, int c) {
	int m = a;
	(void)((m > b) && (m = b));
	(void)((m > c) && (m = c));
	return m;
}

//Function that detects whether a pixel belongs to the skin based on RGB values
void mySkinDetect(Mat& src, Mat& dst) {
	//Surveys of skin color modeling and detection techniques:
	//Vezhnevets, Vladimir, Vassili Sazonov, and Alla Andreeva. "A survey on pixel-based skin color detection techniques." Proc. Graphicon. Vol. 3. 2003.
	//Kakumanu, Praveen, Sokratis Makrogiannis, and Nikolaos Bourbakis. "A survey of skin-color modeling and detection methods." Pattern recognition 40.3 (2007): 1106-1122.
	for (int i = 0; i < src.rows; i++){
		for (int j = 0; j < src.cols; j++){
			//For each pixel, compute the average intensity of the 3 color channels
			Vec3b intensity = src.at<Vec3b>(i, j); //Vec3b is a vector of 3 uchar (unsigned character)
			int B = intensity[0]; int G = intensity[1]; int R = intensity[2];
			if ((R > 95 && G > 40 && B > 20) && (myMax(R, G, B) - myMin(R, G, B) > 15) && (abs(R - G) > 15) && (R > G) && (R > B)){
				dst.at<uchar>(i, j) = 255;
			}
		}
	}
}
