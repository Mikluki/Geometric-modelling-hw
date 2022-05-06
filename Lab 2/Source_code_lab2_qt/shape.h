#ifndef SHAPE_H
#define SHAPE_H

#include "Matrix.h"
#include <vector>
#include "drawlinealgorithms.h"

using namespace std;


// shape in 2d space
class Shape2D
{
public:
    vector<Vect2f> Vertexes; // coordiantes of vertices // Координаты вершин
    Shape2D ()
    {}
    Shape2D (vector<Vect2f> new_vertexes)
    {
        Vertexes = new_vertexes;
    }

    // Drawing this shape
    void Draw(QImage* img,QRgb color)
    {

        for (int i=0; i < Vertexes.size()-1; i++)
        {
            Vect2f& prevPoint = Vertexes[i];
            Vect2f& nextPoint = Vertexes[i+1];

            Drawline(prevPoint.x,prevPoint.y,nextPoint.x,nextPoint.y,color,img);
        }
        if (Vertexes.size() > 0)
            Drawline(Vertexes[Vertexes.size()-1].x,Vertexes[Vertexes.size()-1].y,Vertexes[0].x,Vertexes[0].y,color,img);

    }



};

#endif // SHAPE_H
