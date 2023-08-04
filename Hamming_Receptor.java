import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.Set;

public class Hamming_Receptor {
    public static int detectError(String arr, int nr) {
        int n = arr.length();
        int res = 0;

        for (int i = 0; i < nr; i++) {
            int val = 0;
            for (int j = 1; j <= n; j++) {
                if ((j & (1 << i)) == (1 << i)) {
                    val = val ^ Character.getNumericValue(arr.charAt(n - j));
                }
            }
            res += val * (int) Math.pow(10, i);
        }

        return Integer.parseInt(String.valueOf(res), 2);
    }

    public static String bitsParidad(String receivedData, int r){

        String data = "";

        for (int i = 0; i < receivedData.length(); i++) {
            if ((i + 1) % (Math.pow(2, r)) != 0) {
                data += receivedData.charAt(i);
            }
        }

        return data;
    }

    public static ArrayList<String> main(String receivedData) {
        // Determine the positions of Redundant Bits
        int m = receivedData.length();
        int r = 0;
        for (int i = 0; i < m; i++) {
            if (Math.pow(2, i) >= m + i + 1) {
                r = i;
                break;
            }
        }

        int errorPosition = detectError(receivedData, r);

        if (errorPosition != 0 && errorPosition <= m) {
            StringBuilder correctedData = new StringBuilder(receivedData);
            int errorBit = m - errorPosition;
            char currentBit = receivedData.charAt(errorBit);
            correctedData.setCharAt(errorBit, (currentBit == '0') ? '1' : '0');
            receivedData = correctedData.toString();

            //System.out.println("Errores Detectado en la posicion: " + errorBit + " (de izquieda a derecha comenzando por 0).");
        }

        // Eliminar los bits de paridad para que quede la trama original
        receivedData = bitsParidad(receivedData, r);
        ArrayList<String> data;

        if (errorPosition == 0) {
            data = new ArrayList<>(List.of(receivedData, "false", "hamming"));

        } else if (errorPosition > 0 && errorPosition <= m) {
            data = new ArrayList<>(List.of(receivedData, "true", "hamming"));

        } else {
            data = new ArrayList<>(List.of(receivedData, "None", "hamming"));
        }

        return data;
        
    }
}
