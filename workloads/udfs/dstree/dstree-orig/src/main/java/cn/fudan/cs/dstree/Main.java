package cn.edu.fudan.cs.dstree;

import cn.edu.fudan.cs.dstree.dynamicsplit.IndexBuilder;
import cn.edu.fudan.cs.dstree.dynamicsplit.IndexExactSearcher;

import java.io.IOException;

public class Main {
    public static void main(String args[]) {

       	if(args.length == 4) {
            String filename = args[0];
            String dataset_size = args[1];
            String indexPath = args[2];
            String threshold = args[3];
            //String buffer_size = args[4];	    
            try {
                System.out.println("#### BUILD ONLY MODE");
                System.out.println("Creating index for file: " + filename);
                System.out.println("Max timeseries per leaf: " + threshold);
	            //IndexBuilder.main(new String[]{filename, threshold, "1", dataset_size, buffer_size,indexPath});
                IndexBuilder.main(new String[]{filename, threshold, "1", dataset_size, indexPath});
            } catch (IOException e) {
                e.printStackTrace();
            } catch (ClassNotFoundException e) {
                e.printStackTrace();
            }
        }
        else if(args.length == 2) {
            String indexPath = args[0];
            String qfilename = args[1];
            try {
                System.out.println("#### QUERY ONLY MODE");
                System.out.println("Querying index using file: " + qfilename);
                IndexExactSearcher.main(new String[]{qfilename, indexPath});
            } catch (IOException e) {
                e.printStackTrace();
            } catch (ClassNotFoundException e) {
                e.printStackTrace();
            }
        }
        else {
            System.out.println("For build and query mode type: ");
            System.out.println("java -jar dstree-1.0-SNAPSHOT.jar [dataset] [size] [index file] [queryset] [threshold]");

            System.out.println("For build only mode type: ");
            System.out.println("java -jar dstree-1.0-SNAPSHOT.jar [dataset] [size] [index file]");

            System.out.println("For query only mode type: ");
            System.out.println("java -jar dstree-1.0-SNAPSHOT.jar [index file] [queryset]");
        }



    }
}
