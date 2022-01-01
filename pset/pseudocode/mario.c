#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //gets value from user
  
    int n;

    do
    {
        n =  get_int("input height: ");
    }


    while (n < 1 || n > 8);

// prints  hash triangle to the right

     
    for (int i = 0; i < n; i++)
    {
        for (int k = n - i ; k > 0 ; k--)
        {
            printf(" ") ; 
        }
            
        for (int j = 0 ; j <= i ; j++)
        {
            printf("#");
        }

        printf("\n");
    }


}


