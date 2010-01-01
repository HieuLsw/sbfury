#include <iostream>
#include <list>

using namespace std;

/* 
 * Metodo para ordenar elementos
 *

int Clase :: operator<(const Clase &other) const
{
    if (this->z < other.z)
        return 1;
    else
        return 0;
}

*/

/*
 
 herencia


    this->Sprite::draw(screen, dx);

*/

int main(void)
{
    list <int> items;
    list <int> :: iterator i;

    items.push_back(1);
    items.push_back(20);
    items.push_back(2);

    for (i=items.begin(); i != items.end(); i++)
        cout << *i << endl;

    cout << "y luego de ordenar" << endl;

    items.sort();

    for (i=items.begin(); i != items.end(); i++)
        cout << *i << endl;

    return 0;
}
