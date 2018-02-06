namespace TR {
	class A {
		void a() {}
	};
	
	class B {
		void b() {}
	};
	
	class C : B, A {
		void a(int p) {}
		void b(int p) {}
	};
}