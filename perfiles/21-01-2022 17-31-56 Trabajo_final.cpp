
#include <iostream>
#include <stdio.h>
#include <stdlib.h>


using namespace std;
const int filas=0;

bool validar_datos(int numero, int minimo, int maximo) // Funci�n que valida que un n�mero se encuentre dentro del rango
{
	bool validado=true; // Bandera para saber si la validaci�n fue correcta o fallo
	if(numero<minimo) // Condici�n para validar si el n�mero es menor al rango
	{
		validado=false;
		cout<<""<<endl;
		cout<<"El numero debe ser >="<<minimo<<" y <="<<maximo<<endl;
		return validado;
	}
	
	if(numero>maximo) // Condici�n para validar si el n�mero es mayor al rango
	{
		validado=false;
		cout<<""<<endl;
		cout<<"El numero debe ser >="<<minimo<<" y <="<<maximo<<endl;
		return validado;
	}
	return validado;
}

int opcion3(){ // Funci�n Opcion 3 del men� para el ingreso del tama�o de la matriz
	int N=0;
	bool validado=false;
	while(validado!=true) // Bucle que se ejecuta mientras no ingrese un tama�o correcto
	{
		cout<<""<<endl;
		cout<<"Ingrese el tamano de la matriz"<<endl;
		cin>>N;
		validado=validar_datos(N, 15, 100); // Llamamos a la funci�n para validar el tama�o ingresado
	}
	return N;
}

int opcion1(int N){ // Funci�n Opcion 1 del men� para el ingreso del tama�o de la figura
	int N_figura=0;
	bool validado=false;
	while(validado!=true) // Bucle que se ejecuta mientras no ingrese un tama�o correcto
	{
		cout<<""<<endl;
		cout<<"Ingrese el tamano interno de la figura"<<endl;
		cin>>N_figura;
		validado=validar_datos(N_figura, 10, N); // Llamamos a la funci�n para validar el tama�o ingresado
	}
	return N_figura;
}

int opcion2(){ //  Funci�nOpcion 2 del men� para el ingreso del n�mero para el relleno de la figura
	int numero=0;
	bool validado=false;
	while(validado!=true) // Bucle que se ejecuta mientras no ingrese un n�mero correcto
	{
		cout<<""<<endl;
		cout<<"Ingrese el numero para rellenar la matriz (1-9)"<<endl;
		cin>>numero;
		validado=validar_datos(numero, 1, 9); // Llamamos a la funci�n para validar el n�mero
	}
	return numero;
}

int opcion4(){ // Funci�n Opcion 4 del men� para el ingreso de la localizaci�n horizontal de la figura
	int localizacion_horizontal=0;
	bool validado=false;
	while(validado!=true) // Bucle que se ejecuta mientras no ingrese una ubicaci�n correcta
	{
		cout<<""<<endl;
		cout<<"Ingrese la localizacion de figura horizontal"<<endl;
		cout<<"1. Izquierda"<<endl;
		cout<<"2. Centro"<<endl;
		cout<<"3. Derecha"<<endl;
		cin>>localizacion_horizontal;
		validado=validar_datos(localizacion_horizontal, 1, 3); // Llamamos a la funci�n para validar la ubicaci�n
	}
	return localizacion_horizontal;
}

int opcion5(){ // Funci�n Opcion 5 del men� para el ingreso de la localizaci�n vertical de la figura
	int localizacion_vertical=0;
	bool validado=false;
	while(validado!=true) // Bucle que se ejecuta mientras no ingrese una ubicaci�n correcta
	{
		cout<<""<<endl;
		cout<<"Ingrese la localizacion de figura vertical"<<endl;
		cout<<"1. Arriba"<<endl;
		cout<<"2. Centro"<<endl;
		cout<<"3. Abajo"<<endl;
		cin>>localizacion_vertical;
		validado=validar_datos(localizacion_vertical, 1, 3); // Llamamos a la funci�n para validar la ubicaci�n
	}
	return localizacion_vertical;
}



void agradecimiento() // Funci�n que muestra en pantalla el agradecimiento 
{
	cout<<""<<endl;
	cout<<"***************************************"<<endl;
	cout<<"  Te agradezco por usar el programa!   "<<endl;
	cout<<"***************************************"<<endl;	
	cout<<""<<endl;
}

void encabezado() // Funci�n que muestra en pantalla el encabezado
{
	cout<<""<<endl;
	cout<<"***************************************"<<endl;
	cout<<"        UNIVERSIDAD DEL AZUAY          "<<endl;
	cout<<"               CARRERA                 "<<endl;
	cout<<"           SEBASTIAN SANCHEZ           "<<endl;
	cout<<"***************************************"<<endl;	
	cout<<""<<endl;
}

void menu() // Funci�n que muestra en pantalla el men�
{
	cout<<""<<endl;
	cout<<""<<endl;
	cout<<"***************************************"<<endl;
	cout<<"                   MENU                "<<endl;
	cout<<"***************************************"<<endl;
	cout<<"1) Cambiar tamano interno de la figura "<<endl;
	cout<<"2) Cambio de numero                    "<<endl;
	cout<<"3) Cambio de dimensiones de la matriz  "<<endl;
	cout<<"4) Localizacion de figura Horizontal   "<<endl;
	cout<<"5) Localizacion de figura Vertical     "<<endl;
	cout<<"6) Imprimir matriz                     "<<endl;
	cout<<"12) Salir                              "<<endl;
	cout<<"***************************************"<<endl;
	cout<<"Ingrese un numero de opcion            "<<endl;
	cout<<"***************************************"<<endl;
}

void imprimir(int matriz[][filas], int N_matriz){ // Funci�n para imprimir matriz
	cout<<"\n";
	cout<<"\n";
	cout<<"\n";
	for(int i=0; i<N_matriz; i++) // Recorremos filas
	{
		for(int j=0; j<N_matriz; j++) //Recorremos columnas
		{ 
	    	cout<<matriz[i][j]<<" ";
		}
		cout<<"\n";
	}
	cout<<"\n";
	cout<<"\n";
	cout<<"\n";
}


int main() // M�todo principal/main
{ 
	int N_matriz = 0; // Variable que contiene el tama�o de la matriz
	int N_figura = 0; // Variable que contiene el tama�o de la figura
	int numero_relleno=0; // Variable que contiene el n�mero de relleno de la figura
	int localizacion_horizontal=0; // Variable que contiene el valor de ubicaci�n horizontalmente de la figura 
	int localizacion_vertical=0; // Variable que contiene el valor de ubicaci�n verticalmente de la figura 

	encabezado(); // Llamamos a funci�n para mostrar encabezado
	N_matriz=opcion3(); // Llamamos a funci�n para obtener tama�o de la matriz
	N_figura=opcion1(N_matriz); // Llamamos a funci�n para obtener tama�o de la figura
	numero_relleno=opcion2(); // Llamamos a funci�n para obtener el n�mero para el relleno de la figura
	localizacion_horizontal=opcion4(); // Llamamos a funci�n para obtener la localizaci�n horizontal de la figura
	localizacion_vertical=opcion5(); // Llamamos a funci�n para obtener la localizaci�n vertical de la figura
	
    string opcion="0"; // Variable para controlar la opci�n ingresada del men�
    while(opcion!="12") // Bucle que se ejecuta mientras no ingrese la opci�n 12 que es para salir
	{
		int matriz[N_matriz][N_matriz]; // Definimos la matriz
		for(int i=0; i<N_matriz; i++){ // Bucle para inicializar la matriz con ceros
	    	for(int j=0; j<N_matriz; j++){
	    		matriz[i][j]=0;
			}
		}
		
		int x=0; // Coordenada x de la matriz para saber desde donde comienza a escribirse la figura de acuerdo a su localizaci�n horizontal
		int y=0; // Coordenada y de la matriz para saber desde donde comienza a escribirse la figura de acuerdo a su localizaci�n vertical
		
		
		if(localizacion_horizontal==1 && localizacion_vertical==1) // Condici�n para asignar valor a coordenadas por localizaci�n izquierda arriba
		{
			x=0;
			y=0;
		}
		if(localizacion_horizontal==2 && localizacion_vertical==1) // Condici�n para asignar valor a coordenadas por localizaci�n centro arriba
		{
			x=(N_matriz-N_figura)/2;
			y=0;
		}
		if(localizacion_horizontal==3 && localizacion_vertical==1) // Condici�n para asignar valor a coordenadas por localizaci�n derecha arriba
		{
			x=(N_matriz-N_figura);
			y=0;
		}
		if(localizacion_horizontal==1 && localizacion_vertical==2) // Condici�n para asignar valor a coordenadas por localizaci�n izquierda centro
		{
			x=0;
			y=(N_matriz-N_figura)/2;
		}
		if(localizacion_horizontal==2 && localizacion_vertical==2) // Condici�n para asignar valor a coordenadas por localizaci�n centro centro
		{
			x=(N_matriz-N_figura)/2;
			y=(N_matriz-N_figura)/2;
		}
		if(localizacion_horizontal==3 && localizacion_vertical==2) // Condici�n para asignar valor a coordenadas por localizaci�n derecha centro
		{
			x=(N_matriz-N_figura);
			y=(N_matriz-N_figura)/2;
		}
		if(localizacion_horizontal==1 && localizacion_vertical==3) // Condici�n para asignar valor a coordenadas por localizaci�n izquierda abajo
		{
			x=0;
			y=(N_matriz-N_figura);
		}
		if(localizacion_horizontal==2 && localizacion_vertical==3) // Condici�n para asignar valor a coordenadas por localizaci�n centro abajo
		{
			x=(N_matriz-N_figura)/2;
			y=(N_matriz-N_figura);
		}
		if(localizacion_horizontal==3 && localizacion_vertical==3) // Condici�n para asignar valor a coordenadas por localizaci�n derecha abajo
		{
			x=(N_matriz-N_figura);
			y=(N_matriz-N_figura);
		}
			
		// Insertamos figura en matriz
		for(int i=0; i<N_figura; i++){ 
	    	for(int j=0; j<(i+1); j++){
	    		matriz[i+y][j+x]=numero_relleno; // Escribimos el n�mero asignado de relleno en las posiciones respectivas
			}
		}
		
		menu(); // Llamamos a la funci�n para mostrar el men�
    	cin>>opcion; // Leemos la opci�n ingresada 

    	if(opcion=="1") // Opci�n 1 para cambio de tamano de figura
    	{
    		N_figura=opcion1(N_matriz);
		}else if(opcion=="2") // Opci�n 2 para cambio de n�mero de relleno
		{
			numero_relleno=opcion2();
		}else if(opcion=="3") // Opci�n 3 para cambio de tamano de matriz
		{
			N_matriz=opcion3();
			filas = N_matriz;
		}else if(opcion=="4") // Opci�n 4 para cambio de localizaci�n horizontal de figura
		{
			localizacion_horizontal=opcion4();
		}else if(opcion=="5"){ // Opci�n 5 para cambio de localizaci�n vertical de figura
			localizacion_vertical=opcion5();
		}else if(opcion=="6"){ // Opci�n 6 para poder imprimir la matriz con la figura
			cout<<"\n";
			cout<<"\n";
			cout<<"\n";
			for(int i=0; i<N_matriz; i++) // Recorremos filas
			{
		    	for(int j=0; j<N_matriz; j++){ //Recorremos columnas
	    			cout<<matriz[i][j]<<" ";
				}
				cout<<"\n";
			}
			cout<<"\n";
			cout<<"\n";
			cout<<"\n";
		}else if(opcion=="12") // Opci�n 12 para mostrar agradecimiento y salir
		{
			agradecimiento();	
		}			
	}

    return 0;
}




