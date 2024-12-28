#include <stdio.h>
#include <time.h>  // 時間計測用
 
#include <math.h>

void toBin(int num){
    int i=0;
    int val=0;
    for(i=8;i>=0;i--){
        val = (num >> i);
        if(val % 2 == 0){
            printf("0");
        }else{
            printf("1");
        }
    }
}


int card2(int n,int m){
    int i,j,k;
    int j2,k2;
    int count=0;
    int sum=0;

    int find=0;


    for(i=1;i<=n;i++){
        
        for(j=1;j<=n;j++){
            if(find){
                find=0;
                break;
            }
            for(k=n;k>=1;k--){



                sum=(i+j+k);
                if(sum==m){
                    find=1;
                    if(k<i){
                        count=count +(i-k+1);
                    }else{
                        count=count +(k-i+1);
                    }
                    break;
                }
            }
        }
        find=0;
    }
    return count;
}

int card3(int n,int m){
    int i,j,k;
    int count=0;
    int sum=0;
    for(i=1;i<=n;i++){
        for(j=1;j<=n;j++){
            k=m-i-j;
            if(1<=k && k <=n){
                count++;
            }

        }
    }
    return count;
}

int card(int n,int m){
    int i,j,k;
    int count=0;
    int sum=0;
    for(i=1;i<=n;i++){
        for(j=1;j<=n;j++){

            if((i+j+n) < m){
                continue;
            }else{
                if((i+j+n/2) < m){
                    for(k=n/2;k<=n;k++){
                        sum=(i+j+k);
                        if(sum==m){
                            count++;
                        continue;
                        }
                    }
                }else{
                    for(k=1;k<=n;k++){
                        sum=(i+j+k);
                        if(sum==m){
                            count++;
                        continue;
                        }
                    }
                }

            }

        }
    }
    return count;
}

void toDec(int bin){
    int i=0;
    int val=0;
    for(i=0;i<32;i++){
        val += (((bin >> i) & 0x00000001) )*pow(2,i);
    }
    printf("%d,%d\n",val,val-bin);
}
int main(){
    printf("--------------------\n");
    clock_t start_time = clock();
    double total_time_taken = 0;

    int sum = card3(3000,4000);//(1000,2000)501498
    //toDec(0b101101010110);

    clock_t end_time = clock();
    double time_taken = ((double)(end_time - start_time)) / CLOCKS_PER_SEC;
    total_time_taken = time_taken;

    printf("Total time taken: %.6f seconds\n", total_time_taken);
    printf("%d\n",sum);

    start_time = clock();
    //
    end_time = clock();
    time_taken = ((double)(end_time - start_time)) / CLOCKS_PER_SEC;
    total_time_taken = time_taken;
    //printf("Total time taken: %.6f seconds\n", total_time_taken);

    printf("--------------------\n");
	return 0;
}