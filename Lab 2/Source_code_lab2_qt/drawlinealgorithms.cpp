#include "drawlinealgorithms.h"


// Draw direct line   АС
void Drawline(int ax,int ay,int cx,int cy,QRgb color, QImage* img)
{
    // Alrogithm Asymmetric digital differential analyzer  //   Несимметричный цифровой дифференциальный анализатор
    float k1, k2, k3, temp;
    int x1, x2, sy,sx,y1, tmp;

    float dx = ax - cx;
    float dy = ay - cy;

    // coordiante selection (X or Y) for calculation and moving  // по какой координате будем идти а какую вычислять
    if( fabs(dx) > fabs(dy) )
    {
        // calc Y coordinate, move along X coordiante // Идем по координате Х, вычисляем Y

        // sort points so that X coordinate will be first // Сортируем точки, что бы координата X первой точки была меньше
        if (ax>cx)
        {
            temp=ay;
            ay=cy;
            cy=temp;
            temp=ax;
            ax=cx;
            cx=temp;
        }


        //  calc tangents // Расчет коэффициентов наклона прямых
        // for AC // Для AC
        k1=(cx-ax)?float(cy-ay)/float(cx-ax):0;


        // move along all columns // Проходим по всем столбцам от AX до CX
        for (sx=ax;sx<=cx;sx++)
        {
            y1=k1*(sx-ax)+ay; // search intersection with AC // поиск пересечения с АС

            img->setPixel(sx,y1,color );
        }

    }
    else
    {
        // move along Y coordiante, calc X xoordinate //  Идем по координате Y, вычисляем X

        // sort points so that Y coordiante will be first // Сортируем точки, что бы координата Y первой точки была меньше
        if (ay>cy)
        {
            temp=ay;
            ay=cy;
            cy=temp;
            temp=ax;
            ax=cx;
            cx=temp;
        }


        // calc tangents // Расчет коэффициентов наклона прямых
        // for AC // Для AC
        k1=(cy-ay)?float(cx-ax)/float(cy-ay):0;


        // move along all rows  // Проходим по всем строкам от AY до CY
        for (sy=ay;sy<=cy;sy++)
        {
            x1=k1*(sy-ay)+ax;// / search intersection with AC // поиск пересечения с АС

            img->setPixel(x1,sy,color );

        }
    }

}
