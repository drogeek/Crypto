#include <iostream>
#include <cstdlib>
#include <gmpxx.h>
#include <gmp.h>

int main(int argc, char* argv[]){
	mpz_class s;
	mpz_class p;
	mpz_ui_pow_ui(s.get_mpz_t(), 2, atoi(argv[1]));
	
	do{
		mpz_nextprime(s.get_mpz_t(),s.get_mpz_t());
		p=s*2-1;
	}while(!mpz_probab_prime_p(p.get_mpz_t(),25));

	std::cout << s << " " << p << std::endl;

	return 0;

}


mpz_class getGenerateur(mpz_class p, mpz_class s){
	mpz_class gen;
	mpz_class reste;
	for( gen = 2; i<p-1 ; gen+=1){
		mpz_powm_ui(reste, gen, 2, p);

	mpz_ui_powm_ui(reste.get_mpz_t(), gen.get_mpz_t(), 2, p)
}
