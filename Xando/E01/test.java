
import java.util.Scanner;

public class test {
	public static void main(String[] args) {
		Scanner scanner = new Scanner(System.in);

		// Decimal to Binary
		System.out.print("Zahl zu Binär: ");
		int decimal = scanner.nextInt();
		System.out.println(Integer.toBinaryString(decimal));

		// Binary to Decimal
		System.out.print("Binär zu Zahl: ");
		String binary = scanner.next();
		System.out.println(Integer.parseInt(binary, 2));
	}
}
