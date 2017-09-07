import java.io.File;
import java.util.Scanner;
import java.util.ArrayList;

public class Test {
	
	
	public static void main(String[] arg) throws Exception {
		ArrayList<Integer> fails = new ArrayList<Integer>();
		
		File dir = new File("tests/input");
		File[] inputs = dir.listFiles();
		for(File input : inputs) {
			File expectedOutput = new File("tests/expectedOutput/" + input.getName().replace("cpp", "outC"));
			File output = new File("tests/" + input.getName().replace("cpp", "out"));
			if (!check(output, expectedOutput)) {
				int testNb = Integer.parseInt("" + input.getName().charAt(input.getName().length() - 5));
				fails.add(testNb);
				System.out.println("added " + testNb);
			}
		}
		if(fails.size() > 0) System.out.print("Failed test(s) are of number(s): ");
		else System.out.println("All tests succeeded");
		for(int i = 0; i < fails.size(); i++) {
			if(i != 0) System.out.print(", ");
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