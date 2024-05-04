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
            <h2 className='w-full text-center mt-5 text-2xl font-bold'>
                {group}
            </h2>
            <div className='mt-8 mx-5 w-auto flex flex-col items-center'>
                <Phone image={images[0]} />
                <div className={`${styles.downloadLabel} text-start border rounded-lg px-4 py-2 mt-2 w-full`}>
                    <a href={images[0].url} target='_blank' rel='noreferrer' className='text-blue-500 underline w-10/12'>
                        {images[0].name} - {images[0].scale}
                    </a>
                    <span className={`${styles.downloadIcon}`}>
                        <DownloadIcon onClick={() => download(images[0].url)} />
                    </span>
                </div>
                {images.map((image, index) => {
                    if (index === 0) {
                        return null;
                    }
                    return (
                        <div className='mt-8 mx-5 w-full flex flex-col items-center' key={index}>
                        <div className={`${styles.downloadLabel} text-start border rounded-lg px-4 py-2 mt-2 w-full`}>
                            <a href={image.url} target='_blank' rel='noreferrer' className='text-blue-500 underline w-10/12'>
                                {image.name} - {image.scale}
                            </a>
                            <span className={`${styles.downloadIcon}`}>
                                <DownloadIcon onClick={() => download(images[0].url)} />
                            </span>
                        </div>
                    </div>
                    )
                })}
            </div>
        </div>
    )
}

export { Show };
