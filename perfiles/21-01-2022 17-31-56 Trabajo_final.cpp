
#include <iostream>
#include <stdio.h>
#include <stdlib.h>


using namespace std;
const int filas=0;

bool validar_datos(int numero, int minimo, int maximo) // Función que valida que un número se encuentre dentro del rango
{
	bool validado=true; // Bandera para saber si la validación fue correcta o fallo
	if(numero<minimo) // Condición para validar si el número es menor al rango
	{
		validado=false;
		cout<<""<<endl;
		cout<<"El numero debe ser >="<<minimo<<" y <="<<maximo<<endl;
		return validado;
	}
	
	if(numero>maximo) // Condición para validar si el número es mayor al rango
	{
		validado=false;
		cout<<""<<endl;
		cout<<"El numero debe ser >="<<minimo<<" y <="<<maximo<<endl;
		return validado;
	}
	return validado;
}

int opcion3(){ // Función Opcion 3 del menú para el ingreso del tamaño de la matriz
	int N=0;
	bool validado=false;
	while(validado!=true) // Bucle que se ejecuta mientras no ingrese un tamaño correcto
	{
		cout<<""<<endl;
		cout<<"Ingrese el tamano de la matriz"<<endl;
		cin>>N;
		validado=validar_datos(N, 15, 100); // Llamamos a la función para validar el tamaño ingresado
	}
	return N;
}

int opcion1(int N){ // Función Opcion 1 del menú para el ingreso del tamaño de la figura
	int N_figura=0;
	bool validado=false;
	while(validado!=true) // Bucle que se ejecuta mientras no ingrese un tamaño correcto
	{
		cout<<""<<endl;
		cout<<"Ingrese el tamano interno de la figura"<<endl;
		cin>>N_figura;
		validado=validar_datos(N_figura, 10, N); // Llamamos a la función para validar el tamaño ingresado
	}
	return N_figura;
}

int opcion2(){ //  FunciónOpcion 2 del menú para el ingreso del número para el relleno de la figura
	int numero=0;
	bool validado=false;
	while(validado!=true) // Bucle que se ejecuta mientras no ingrese un número correcto
	{
		cout<<""<<endl;
		cout<<"Ingrese el numero para rellenar la matriz (1-9)"<<endl;
		cin>>numero;
		validado=validar_datos(numero, 1, 9); // Llamamos a la función para validar el número
	}
	return numero;
}

int opcion4(){ // Función Opcion 4 del menú para el ingreso de la localización horizontal de la figura
	int localizacion_horizontal=0;
	bool validado=false;
	while(validado!=true) // Bucle que se ejecuta mientras no ingrese una ubicación correcta
	{
		cout<<""<<endl;
		cout<<"Ingrese la localizacion de figura horizontal"<<endl;
		cout<<"1. Izquierda"<<endl;
		cout<<"2. Centro"<<endl;
		cout<<"3. Derecha"<<endl;
		cin>>localizacion_horizontal;
		validado=validar_datos(localizacion_horizontal, 1, 3); // Llamamos a la función para validar la ubicación
	}
	return localizacion_horizontal;
}

int opcion5(){ // Función Opcion 5 del menú para el ingreso de la localización vertical de la figura
	int localizacion_vertical=0;
	bool validado=false;
	while(validado!=true) // Bucle que se ejecuta mientras no ingrese una ubicación correcta
	{
		cout<<""<<endl;
		cout<<"Ingrese la localizacion de figura vertical"<<endl;
		cout<<"1. Arriba"<<endl;
		cout<<"2. Centro"<<endl;
		cout<<"3. Abajo"<<endl;
		cin>>localizacion_vertical;
		validado=validar_datos(localizacion_vertical, 1, 3); // Llamamos a la función para validar la ubicación
	}
	return localizacion_vertical;
}



void agradecimiento() // Función que muestra en pantalla el agradecimiento 
{
	cout<<""<<endl;
	cout<<"***************************************"<<endl;
	cout<<"  Te agradezco por usar el programa!   "<<endl;
	cout<<"***************************************"<<endl;	
	cout<<""<<endl;
}

void encabezado() // Función que muestra en pantalla el encabezado
{
	cout<<""<<endl;
	cout<<"***************************************"<<endl;
	cout<<"        UNIVERSIDAD DEL AZUAY          "<<endl;
	cout<<"               CARRERA                 "<<endl;
	cout<<"           SEBASTIAN SANCHEZ           "<<endl;
	cout<<"***************************************"<<endl;	
	cout<<""<<endl;
}

void menu() // Función que muestra en pantalla el menú
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

void imprimir(int matriz[][filas], int N_matriz){ // Función para imprimir matriz
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


int main() // Método principal/main
{ 
	int N_matriz = 0; // Variable que contiene el tamaño de la matriz
	int N_figura = 0; // Variable que contiene el tamaño de la figura
	int numero_relleno=0; // Variable que contiene el número de relleno de la figura
	int localizacion_horizontal=0; // Variable que contiene el valor de ubicación horizontalmente de la figura 
	int localizacion_vertical=0; // Variable que contiene el valor de ubicación verticalmente de la figura 

	encabezado(); // Llamamos a función para mostrar encabezado
	N_matriz=opcion3(); // Llamamos a función para obtener tamaño de la matriz
	N_figura=opcion1(N_matriz); // Llamamos a función para obtener tamaño de la figura
	numero_relleno=opcion2(); // Llamamos a función para obtener el número para el relleno de la figura
	localizacion_horizontal=opcion4(); // Llamamos a función para obtener la localización horizontal de la figura
	localizacion_vertical=opcion5(); // Llamamos a función para obtener la localización vertical de la figura
	
    string opcion="0"; // Variable para controlar la opción ingresada del menú
    while(opcion!="12") // Bucle que se ejecuta mientras no ingrese la opción 12 que es para salir
	{
		int matriz[N_matriz][N_matriz]; // Definimos la matriz
		for(int i=0; i<N_matriz; i++){ // Bucle para inicializar la matriz con ceros
	    	for(int j=0; j<N_matriz; j++){
	    		matriz[i][j]=0;
			}
		}
		
		int x=0; // Coordenada x de la matriz para saber desde donde comienza a escribirse la figura de acuerdo a su localización horizontal
		int y=0; // Coordenada y de la matriz para saber desde donde comienza a escribirse la figura de acuerdo a su localización vertical
		
		
		if(localizacion_horizontal==1 && localizacion_vertical==1) // Condición para asignar valor a coordenadas por localización izquierda arriba
		{
			x=0;
			y=0;
		}
		if(localizacion_horizontal==2 && localizacion_vertical==1) // Condición para asignar valor a coordenadas por localización centro arriba
		{
			x=(N_matriz-N_figura)/2;
			y=0;
		}
		if(localizacion_horizontal==3 && localizacion_vertical==1) // Condición para asignar valor a coordenadas por localización derecha arriba
		{
			x=(N_matriz-N_figura);
			y=0;
		}
		if(localizacion_horizontal==1 && localizacion_vertical==2) // Condición para asignar valor a coordenadas por localización izquierda centro
		{
			x=0;
			y=(N_matriz-N_figura)/2;
		}
		if(localizacion_horizontal==2 && localizacion_vertical==2) // Condición para asignar valor a coordenadas por localización centro centro
		{
			x=(N_matriz-N_figura)/2;
			y=(N_matriz-N_figura)/2;
		}
		if(localizacion_horizontal==3 && localizacion_vertical==2) // Condición para asignar valor a coordenadas por localización derecha centro
		{
			x=(N_matriz-N_figura);
			y=(N_matriz-N_figura)/2;
		}
		if(localizacion_horizontal==1 && localizacion_vertical==3) // Condición para asignar valor a coordenadas por localización izquierda abajo
		{
			x=0;
			y=(N_matriz-N_figura);
		}
		if(localizacion_horizontal==2 && localizacion_vertical==3) // Condición para asignar valor a coordenadas por localización centro abajo
		{
			x=(N_matriz-N_figura)/2;
			y=(N_matriz-N_figura);
		}
		if(localizacion_horizontal==3 && localizacion_vertical==3) // Condición para asignar valor a coordenadas por localización derecha abajo
		{
			x=(N_matriz-N_figura);
			y=(N_matriz-N_figura);
		}
			
		// Insertamos figura en matriz
		for(int i=0; i<N_figura; i++){ 
	    	for(int j=0; j<(i+1); j++){
	    		matriz[i+y][j+x]=numero_relleno; // Escribimos el número asignado de relleno en las posiciones respectivas
			}
		}
		
		menu(); // Llamamos a la función para mostrar el menú
    	cin>>opcion; // Leemos la opción ingresada 

    	if(opcion=="1") // Opción 1 para cambio de tamano de figura
    	{
    		N_figura=opcion1(N_matriz);
		}else if(opcion=="2") // Opción 2 para cambio de número de relleno
		{
			numero_relleno=opcion2();
		}else if(opcion=="3") // Opción 3 para cambio de tamano de matriz
		{
			N_matriz=opcion3();
			filas = N_matriz;
		}else if(opcion=="4") // Opción 4 para cambio de localización horizontal de figura
		{
			localizacion_horizontal=opcion4();
		}else if(opcion=="5"){ // Opción 5 para cambio de localización vertical de figura
			localizacion_vertical=opcion5();
		}else if(opcion=="6"){ // Opción 6 para poder imprimir la matriz con la figura
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
		}else if(opcion=="12") // Opción 12 para mostrar agradecimiento y salir
		{
			agradecimiento();	
		}			
	}

    return 0;
}




