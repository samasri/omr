namespace OMR {
class A {
	void f() {}
	void h(int) {}
	void h() {}
};
}

namespace Ruby {
class A : OMR::A {
	void f() {}
	void h() {}
};
}

namespace TR {
class A : Ruby::A {
	void f(int) {}
	void h(int) {}
	void h() {}
};
}