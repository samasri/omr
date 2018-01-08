namespace noName {
class A {
	void a() {}
	void b() {}
	void a(int a1) {}
};
}
namespace TR {
class B : noName::A {
	void a() {}
	void a(int a1) {}
};
}