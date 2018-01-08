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
	void h(int) {}
};
}

namespace TR {
class A : Ruby::A {
	void f() {}
	void h(int) {}
	void h() {}
};
}