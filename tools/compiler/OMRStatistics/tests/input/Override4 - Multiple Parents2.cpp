namespace TR {
	class A {
		void a() {}
	};
	
	class B : A {
		void b() {}
	};
	
	class C : B, A {
		void a() {}
		void b() {}
	};
}