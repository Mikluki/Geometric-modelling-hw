//---------------------------------------------------------------------------

#ifndef MatrixH
#define MatrixH
//---------------------------------------------------------------------------


class Matrix3f;


class Vect2f // class of the coorinates in 2D space // Класс для представления векторов в 2х мерном пространстве
{
  public:
    float x, y, w ; // homogeneous coordinates

     Vect2f  (float x=0, float y=0, float w=0);
     Vect2f   operator*( Matrix3f& m); //Операция умножения вектора на матрицу 4х4

   float&   operator[](int i);
};

class Matrix3f
{
  public:
  Vect2f M[3]; // rows and columns of the matrix // Представляем матрицу 3х3 как совокупность 3-х векторов 3х1

  Matrix3f()
  {}// Конструктор без параметров (создает единичную матрицу)


  Matrix3f operator*(Matrix3f& a); // multiplication of 2 matices// Определение операции умножения двух матриц
  Vect2f& operator[](int i) ;   // access to elements // Определение операции доступа к элементам матрицы
  void identity(void);  // set identity //Функция делает единичную матрицу
  double determinant (); // determinant//  Детерминант
};


#endif
