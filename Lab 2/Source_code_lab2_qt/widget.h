#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <shape.h>

#include <QTimer>


namespace Ui {
class Widget;
}


class Widget : public QWidget
{
    Q_OBJECT

public:
    explicit Widget(QWidget *parent = nullptr);
    ~Widget();

    Shape2D shape;
    QImage* img;
    QTimer* timer;
    int direction_x=1;
    int direction_y=1;
    int rotate=5;
    void Init();
    void RotateShape( float addAngle );
    void MoveShape(float addX,float addY);
    void DrawScene();
private slots:


    void on_pushButton_RotateClockwise_clicked();

    void on_pushButton_RotateCounterclockwise_clicked();

    void on_pushButton_X_add_clicked();

    void on_pushButton_X_sub_clicked();

    void on_pushButton_Y_add_clicked();

    void on_pushButton_Y_sub_clicked();


    private slots:
        void TimerInterval();

        void on_pushButton_startTimer_clicked();

private:
    Ui::Widget *ui;
};

#endif // WIDGET_H
