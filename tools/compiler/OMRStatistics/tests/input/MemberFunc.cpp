//Reproducing the case in Matthew's argument, about foreseen challenges for changing from static to dynamic polymorphism in some cases. For more information, check Matthew's argument, under the "Known Challenges" section: "https://github.com/ualberta-smr/paper-almasri-SPLC/blob/master/Matthew's%20argument/Matthew's%20Argument.pdf"

namespace OMR {
	class X {
	public:
		int a() {
			return 0;
		}
		int b() {
			return 1;
		}
	};
	
	namespace X86 {
		class X : public OMR::X {
		public:
			int a() {
				return 1;
			}
		};
	}
	
	namespace Power {
		class X : public OMR::X {
		public:
			int a() {
				return 2;
			}
		};
	}
	
	namespace Z {
		class X : public OMR::X {
		public:
			int a() {
				this->a();
				return 3;
			}
		};
	}
}

namespace TR {
	class X : public OMR::X86::X {
		
	};
}

/*int OMR::X::b() {
	//TR::X* self = static_cast<TR::X *>(this);
	//self->a();
	//this->a();
	return 0;		
	//return -1;//self->a();
}*/

/*int OMR::Z::X::a() {
	this->a();
	return 3;
}*/