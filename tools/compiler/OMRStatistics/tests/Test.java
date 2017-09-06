import java.io.File;
import java.util.Scanner;
import java.util.ArrayList;

public class Test {
	
	final static int NB_OF_TESTS = 5;
	
	public static void main(String[] arg) throws Exception {
		ArrayList<Integer> fails = new ArrayList<Integer>();
		for(int i = 1; i <= NB_OF_TESTS; i++) {
			String name = "tests/test" + i;
			if (!check(new File(name + ".out"), new File(name + ".outC"))) 
				fails.add(i);
		}
		if(fails.size() > 0) System.out.print("Failed tests are of numbers: ");
		else System.out.println("All tests succeeded");
		for(int i = 0; i < fails.size(); i++) {
			if(i != 0) System.out.print(", " + fails.get(i));
			System.out.print(fails.get(i));
		}
		System.out.println();
	}
	
	public static boolean check(File f1, File f2) throws Exception {
		Scanner s1 = new Scanner(f1);
		Scanner s2 = new Scanner(f2);
		while (s1.hasNextLine()) {
			if(!s2.hasNextLine()) return false;
			String c1 = s1.nextLine();
			String c2 = s2.nextLine();
			if(!c1.equals(c2)) return false;
		}
		return true;
	}
}