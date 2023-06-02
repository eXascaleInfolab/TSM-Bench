package cn.edu.fudan.cs.dstree.util.system;


/**
 * A factory that will produce a working RuntimeInformation if you are using a 1.5 or better JVM. If not then it will
 * return stub that only returns zeros.
 */
public class RuntimeInformationFactory {
    private static final RuntimeInformation runtimeInformationBean = canGenerateRuntimeInformationBean() ? new RuntimeInformationBean() : new RuntimeInformationStub();

    /**
     * @return produce a RuntimeInformationBean if you are using a 1.5 or better JVM. If not then it will
     *         return null.
     */
    public static RuntimeInformation getRuntimeInformation() {
        return runtimeInformationBean;
    }

    static boolean canGenerateRuntimeInformationBean() {
        try {
            return true;
        } catch (final Exception e) {
            return false;
        }
    }
}
