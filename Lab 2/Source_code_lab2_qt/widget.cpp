#include "widget.h"
#include "ui_widget.h"
#include <QtGui>
#include <QPixmap>
#include "shape.h"





Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);

    Init();
}

Widget::~Widget()
{
    delete ui;
}

void Widget::Init()
{
    img = NULL;

    img = new QImage(ui->label->width(),ui->label->height(), QImage::Format_RGB888);
    img->fill(QColor(Qt::white).rgb());

    srand(static_cast<unsigned int>(time(0))) ;
    float k;
    QRect r = img->rect();
    k=float(r.right()*0.5)/float(RAND_MAX);

    // Construct our shape using random coordinates
    shape.Vertexes.push_back({rand()*k,rand()*k,1});
    shape.Vertexes.push_back({rand()*k,rand()*k,1});
    shape.Vertexes.push_back({rand()*k,rand()*k,1});


    timer = new QTimer();
    timer->setInterval(100);
    // bind event with handler //  Соединяем событие с обработчиком
    connect(timer, SIGNAL(timeout()), this, SLOT(TimerInterval()));


}



void Widget::DrawScene()
{
    // set colot of shape
    QRgb color = qRgb(255,0,0);

    // clear canvas
    img->fill(QColor(Qt::white).rgb());

    // Draw our shape
    shape.Draw(img,color);

    // put new canvas in the GUI component
    ui->label->setPixmap(QPixmap::fromImage(*img));
    ui->label->update();
}

void Widget::RotateShape( float RotationAnglePhi )
{


    Matrix3f mv,transM1,transM2,rotateM ;   // transformation matrices
    Vect2f operand, result;
    float cosf, sinf,phiRadians;

     // set identity matrices  // Делаем все матрицы единичными
    mv.identity(); transM1.identity(); transM2.identity();
    rotateM.identity();

    // calculate the angle in radians.  Переводим в радианы
    phiRadians = RotationAnglePhi *0.01571;

    cosf = cos(phiRadians);
    sinf = sin(phiRadians);
    rotateM[0][0] = cosf;
    rotateM[0][1] = sinf;
    rotateM[1][0] = -sinf;
    rotateM[1][1] = cosf;


    // Translation matrix. Moving to new point // Матрица переноса начала координат в заданную точку
    transM1[2][0]=-shape.Vertexes[0].x;
    transM1[2][1]=-shape.Vertexes[0].y;

    // Translation matrix. Moving back // Матрица переноса начала координат обратно
     transM2[2][0]=shape.Vertexes[0].x;
     transM2[2][1]=shape.Vertexes[0].y;

     mv = transM1*rotateM*transM2;

    for (int i=0;i<shape.Vertexes.size();i++) //Apply matrix to all vertices
    {
      operand=shape.Vertexes[i];
      result=operand*mv;
      shape.Vertexes[i]=result;  //Save new vertices
    }
}


void Widget::MoveShape(float addX,float addY)
{
    Matrix3f mv,transM1;   // transformation matrices // Матрицы   преобразования
    Vect2f operand, result;
    float cosf, sinf,phiRadians;

    // set identity matrices  // Делаем все матрицы единичными
    mv.identity(); transM1.identity();

    // Translation matrix. Moving to new point // Матрица переноса начала координат в заданную точку
    transM1[2][0]= addX;
    transM1[2][1]= addY;


     mv = transM1;

    for (int i=0;i<shape.Vertexes.size();i++) //Apply matrix to all vertices //Применяем матрицу mv ко всем вершинам
    {
      operand=shape.Vertexes[i];
      result=operand*mv;
      shape.Vertexes[i]=result; //Save new vertices
    }

}



void Widget::on_pushButton_RotateClockwise_clicked()
{
    RotateShape(3);
    DrawScene();
}

void Widget::on_pushButton_RotateCounterclockwise_clicked()
{
    RotateShape(-3);
    DrawScene();
}

void Widget::on_pushButton_X_add_clicked()
{
    MoveShape(5,0);
    DrawScene();
}

void Widget::on_pushButton_X_sub_clicked()
{
    MoveShape(-5,0);
    DrawScene();
}

void Widget::on_pushButton_Y_add_clicked()
{
    MoveShape(0,-5);
    DrawScene();
}

void Widget::on_pushButton_Y_sub_clicked()
{
    MoveShape(0,5);
    DrawScene();
}

void Widget::TimerInterval()
{
    QRect boundingbox = img->rect();



    for (int i=0; i< shape.Vertexes.size(); i++)
    {
        if (shape.Vertexes[i].x > boundingbox.right() ||
                shape.Vertexes[i].x < boundingbox.left()

                )
        {

            direction_x = -direction_x;
            rotate= -rotate;
        }

        if ( shape.Vertexes[i].y > boundingbox.bottom()  ||
             shape.Vertexes[i].y < boundingbox.top())
        {
            direction_y = -direction_y;
            rotate= -rotate;
        }
    }

    RotateShape(rotate);
    MoveShape(direction_x,direction_y);
    DrawScene();
}

void Widget::on_pushButton_startTimer_clicked()
{
    if (!timer->isActive())
        timer->start();
    else
        timer->stop();
}
