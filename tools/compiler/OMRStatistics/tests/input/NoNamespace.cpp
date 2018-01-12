namespace TR {
	class A {
		void a() {}
		void a(int param) {}
	};
}
	
class B : TR::A {
	void a() {}
	void b() {}
	void b(int) {}
};