import { useEffect, useMemo } from 'react';
import { useStates } from '../../Hooks/useStates';
import { Phone } from '../../Components/Cards/Phone';
import { DownloadIcon } from '../../Components/Icons';
import { DobleLoader } from '../../Components/Loaders/DobleLoader';
import styles from './styles/index.module.scss';

const Show = props => {
    const { ls, lf, s, f, useParams } = useStates();

    const images = useMemo(() => s.app?.show?.images || [], [s.app?.show?.images]);
    const loading = useMemo(() => s.loaders?.app?.getGroupImages ?? true, [s.loaders?.app?.getGroupImages]);
    // const images = s.app?.show?.images || [];
    // console.log(images);

    const { group } = useParams();

    const download = url => {
        const name = url.split('/').pop();
        const a = document.createElement('a');
        a.href = url;
        a.download = name;
        a.click();
    };

    useEffect(() => {
        f.app.getGroupImages(group);
    }, [group]);

    if (loading) {
        return (
            <div className='w-full flex justify-center mt-16'>
                <DobleLoader />
            </div>
        );
    }

    if (images.length === 0) {
        return (
            <div className='w-full flex justify-center mt-16'>
                <h2 className='text-2xl font-bold'>No se encontraron imágenes</h2>
            </div>
        );
    }

    return (
        <div className='flex flex-wrap justify-around mb-5'>
            <h2 className='w-full text-center mt-5 text-4xl font-bold'>
                {group}
            </h2>
            <div className='w-10/12 flex flex-col items-center mt-4'>
                <Phone image={images[0]} block={true} alone={true} />
            </div>
            <div className='mt-8 w-11/12 mx-5 flex flex-col items-center lg:flex-row lg:flex-wrap lg:justify-center' >
                {images.map((image, index) => {
                    return (
                        <div className={`${styles.downloadLabel} text-start border rounded-lg px-5 py-3 mb-4 mx-3 w-8/12 lg:w-1/4`} key={index}>
                            <a href={image.url} target='_blank' rel='noreferrer' className='text-blue-500 underline w-10/12'>
                                {image.name} - {image.scale}
                            </a>
                            <span className={`${styles.downloadIcon}`}>
                                <DownloadIcon onClick={() => download(images[0].url)} />
                            </span>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}

export { Show };
