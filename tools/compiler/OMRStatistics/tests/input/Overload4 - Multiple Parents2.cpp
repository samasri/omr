namespace TR {
	class A {
		void a() {}
		void a(int param) {}
	};
	
	class B : A {
		void b() {}
	};
	
	class C : B, A {
		void a(int p) {}
		void b(int p) {}
	};
}