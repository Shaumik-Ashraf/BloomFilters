//parse_url_data.c 
//parse the malicious_n_nonmalicious url dataset from kaggle to be just urls
//for Algo Bloom Filter project
//see: https://www.kaggle.com/antonyj453/urldataset 

#include<stdio.h> 
#include<stdlib.h>
#include<string.h>

#define MAX 3000

int main(int argc, char** argv) {
	
	char buf1[MAX-1];
	char buf2[MAX];
	size_t len_to_cpy;
	FILE* in;
	FILE* out;
	
	if( argc < 3 ) {
		printf("Usage: %s <data file> <output file>\n", argv[0]);
		exit(1);
	}
	
	in = fopen(argv[1], "r");
	out = fopen(argv[2], "w");
	
	printf("Reading %s; writing to %s...", argv[1], argv[2]);
	while( fgets(buf1, MAX-2, in) ) {
		if( !strpbrk(buf1, ",/ \t\n//\\") ) {
			perror("1");
			abort();
		}
		len_to_cpy = (size_t)(strpbrk(buf1, ",/ \t\n//\\") - buf1);
		if( len_to_cpy > (MAX - 1) ) {
			perror("2");
			abort();
		}
		strncpy(buf2, buf1, len_to_cpy);
		buf2[len_to_cpy] = '\0';
		printf("%s\n", buf2);
		fprintf(out, "%s\n", buf2);
	}
	fclose(in);
	fclose(out);
	
	return(0);
}