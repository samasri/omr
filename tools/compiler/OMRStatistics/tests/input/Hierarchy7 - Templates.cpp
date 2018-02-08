template <class T>
class mypair;

template <class T>
class mypair {
  public:
    T values [2];
    mypair (T first, T second) {
      values[0]=first; values[1]=second;
    }
};


class A : mypair<int> {
	
};