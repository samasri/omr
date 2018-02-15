namespace OMR {
	class A {
		virtual void a() {}
	};
}

namespace X86 {
	class A : OMR::A {
		void a() {}
	};
}

namespace TR {
	class A : X86::A {
		void a() {}
	};
}