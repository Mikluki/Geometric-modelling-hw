//---------------------------------------------------------------------------




#include "Matrix.h"
//---------------------------------------------------------------------------


Vect2f::Vect2f(float x, float y, float w) :x(x),y(y),w(w)
{
}

Vect2f Vect2f::operator *(Matrix3f& m)
{

  Vect2f Res;
  int i=0;

    for (i=0;i<= 2;i++)
      Res[i] =x*m[0][i]+y*m[1][i]+w*m[2][i];
  return Res;
}

float& Vect2f::operator[](int i)  // access to elements // Определение операции доступа к элементам матрицы
{
    switch (i)
    {
      case 0: return x; //[0]
      case 1: return y; //[1]
      case 2: return w; //[2]
       //Если индекс за границей массива, то формируем исключение
      default: throw  "Invalid index" ;
    }
}

double Matrix3f::determinant(void)
{
    double det =
    (M[0][0]*M[1][1]*M[2][2] +
                M[2][0]*M[0][1]*M[1][2] +
                M[0][2]*M[1][0]*M[2][1]) -
               (M[2][0]*M[1][1]*M[0][2] +
                M[2][2]*M[1][0]*M[0][1] +
                M[0][0]*M[1][2]*M[2][1]);

    return det;
}

 Vect2f& Matrix3f::operator[](int i) // Определение операции доступа к элементам матрицы
 {
     if ((i<0)||(i>3))
       throw  "Неверный индекс" ;
     else
       return M[i];
 }

 void Matrix3f::identity(void)  // Функция делает единичную матрицу
 {
   int i, j;
   for (i=0; i<3; i++)
     for (j=0; j<3; j++)
       if (i==j)
         M[i][j]=1;
       else
         M[i][j]=0;
 }

 Matrix3f Matrix3f::operator*(Matrix3f& a) // Определение операции умножения двух матриц
 {
   Matrix3f t;
   int i;
   for (i=0; i<3; i++)
   {
          t[i]=M[i]*a;
   }
   return t;
 }




