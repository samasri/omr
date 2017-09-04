import java.io.File;
import java.util.Scanner;

public class Test {
	
	public static void main(String[] arg) throws Exception {
		System.out.println("Hello World!");
		File f1 = new File("test1.out");
		File f2 = new File("test1.outC");
		if(check(f1, f2)) System.out.println("Passed");
		else System.out.println("Failed");
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