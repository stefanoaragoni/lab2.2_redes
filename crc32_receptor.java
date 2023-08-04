import java.util.ArrayList;
import java.util.List;

public class crc32_receptor {
    public static String crc32(String trama) {
        String polinomioStr = "111011011011100010000011001000001";
        int SIZE = 32;

        List<Integer> polinomio = new ArrayList<>();
        for (char bit : polinomioStr.toCharArray()) {
            polinomio.add(Character.getNumericValue(bit));
        }

        List<Integer> data = new ArrayList<>();
        for (char bit : trama.toCharArray()) {
            data.add(Character.getNumericValue(bit));
        }

        // Valores a utilizar
        List<Integer> dataCalc = new ArrayList<>(data.subList(0, polinomio.size()));
        data = new ArrayList<>(data.subList(polinomio.size(), data.size()));

        // polinomio | data
        while (true) {
            // Se eliminan los bits no significativos
            int eliminados = 0;
            while (dataCalc.size() > 0 && dataCalc.get(0) == 0) {
                dataCalc.remove(0);
                eliminados++;
            }

            // Se agregan los bits a dataCalc para que sea del mismo tamaño que el polinomio
            for (int i = 0; i < eliminados; i++) {
                // Si ya no hay bits en data, se termina el proceso
                if (data.isEmpty()) {
                    break;
                } else {
                    int bit = data.remove(0);
                    dataCalc.add(bit);
                }
            }

            // Si dataCalc es menor que el polinomio, se termina el proceso
            if (dataCalc.size() < polinomio.size()) {
                // Si ya no hay bits en data, se termina el proceso
                if (data.isEmpty()) {
                    // Se agregan 0 al inicio de dataCalc para que sea del mismo tamaño que el polinomio
                    while (dataCalc.size() < SIZE) {
                        dataCalc.add(0, 0);
                    }
                    break;
                }
            }

            // Si dataCalc es igual al polinomio, se hace XOR entre ambos
            if (dataCalc.size() == polinomio.size()) {
                for (int i = 0; i < polinomio.size(); i++) {
                    dataCalc.set(i, dataCalc.get(i) ^ polinomio.get(i));
                }
            }
        }

        // Convert the result back to a string representation
        StringBuilder crc = new StringBuilder();
        for (int bit : dataCalc) {
            crc.append(bit);
        }

        return crc.toString();
    }

    public static void main(String[] args) {
        System.out.println("\n---------- CRC32 Receptor ----------\n");
        
        String trama = System.console().readLine("Trama: ");
        trama = trama.replaceAll(" ", "");

        String encoded = crc32(trama);

        // Revisar si encoded tiene 1s, si es así, la trama está mal
        boolean error = false;
        for (char bit : encoded.toCharArray()) {
            if (bit == '1') {
                error = true;
                break;
            }
        }

        if (error) {
            System.out.println("\nResultado: Error en la trama | "+ encoded +"\n");
        } else {
            System.out.println("\nResultado: Trama sin errores | "+ encoded +"\n");
        }
    }
}
