#include "widget.h"
#include <QApplication>
#include <QtGui>
#include <QLabel>




int main(int argc, char *argv[])
{

    QApplication a(argc, argv);
    Widget w;
    w.show();
    return a.exec();

}
