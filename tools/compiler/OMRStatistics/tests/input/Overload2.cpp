namespace TR {
	class D {
		void a() {}
		void b() {}
		void c() {}
		void d() {}
	};

	class C : D{
		void a() {}
	};

	class B : C{
		void a() {}
		void a(int param) {}
	};

	class A : B{
		
	};
}