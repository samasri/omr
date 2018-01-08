namespace TR {
	class A {
		void a() {
			return;
		}
	};
	
	class B : A {
		void b() {}
	};

	class C : B {
		void a() {}
	};
}