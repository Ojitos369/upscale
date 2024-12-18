import axios from "axios";
import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';
import { useDispatch, useSelector } from "react-redux";
import { f as ff } from "./fs";


const MySwal = withReactContent(Swal);

const link = 'http://localhost:8369/api/';
axios.defaults.withCredentials = true
const miAxios = axios.create({
    baseURL: link,
});


const useF = props => {
    const ls = useSelector(state => state.fs.ls);
    const s = useSelector(state => state.fs.s);
    const d = useDispatch();

    const login = {
        login: () => {
            u2('loaders', 'login', 'login', true);
            const end = 'user/login/';
            const data = s.menu?.login;
            u2('menu', 'login', 'error', '');

            miAxios.post(end, data)
            .then(response => {
                const user = response.data.user;
                const token = user.token;
                document.cookie = `tups=${token}; max-age=18000; path=/`;
                u2('menu', 'modal', 'mode', 'menu');
                u1('menu', 'login', {});
                u2('login', 'data', 'user', user);
                u2('modals', 'header', 'showMenu', false);
            }).catch(error => {
                const message = error.response.data.message;
                u2('menu', 'login', 'error', message);
            }).finally(() => {
                u2('loaders', 'login', 'login', false);
            });
        },
        validateLogin: () => {
            const end = 'user/validate_login/';
            // get tups cookie
            miAxios.get(end)
            .then(response => {
                const user = response.data.user;
                u2('login', 'data', 'user', user);
            }).catch(error => {
                // console.log(error);
                u2('login', 'data', 'user', {});
                document.cookie = `tups=; max-age=0; path=/`;
            })
        },
        closeSession: () => {
            u2('loaders', 'login', 'closeSession', true);
            const end = 'user/close_session/';

            miAxios.get(end)
            .finally(() => {
                u2('login', 'data', 'user', {});
                document.cookie = 'tups=; max-age=0; path=/';
                u2('modals', 'header', 'showMenu', false);
                u2('loaders', 'login', 'closeSession', false);
            });
        }
    }

    const app = {
        getCategorias: () => {
            const end = 'app/get_categorias/';
            miAxios.get(end)
            .then(res => {
                const categorias = res.data;
                u2('app', 'data', 'categorias', categorias);
            })
            .catch(err => {
                console.log(err);
            });
        },
        getImages: () => {
            if (!!s.loaders?.app?.getImages) return;

            u2('loaders', 'app', 'getImages', true);

            let filtros = {...s.app?.filtros || {}};
            // console.log('filtros', filtros);
            const paginador = {...s.app?.paginador || {}};
            const pagina = paginador.pagina || 1;
            const por_pagina = paginador.por_pagina || 20;

            filtros.pagina = pagina;
            filtros.por_pagina = por_pagina;

            // console.log("filtros", filtros);
            let end = `app/get_images/?pagina=${pagina}&por_pagina=${por_pagina}`;

            if (!!filtros.cats) {
                if (typeof filtros.cats === 'list') {
                    if ((filtros.cats || []).length > 0) {
                        // join cats with ',
                        const cats = filtros.cats.join(',');
                        end += `&cats=${cats}`;
                    }
                } else {
                    end += `&cats=${filtros.cats}`;
                }
            }
            if (!!filtros.name) {
                end += `&name=${filtros.name}`;
            }
            if (!!filtros.model) {
                end += `&model=${filtros.model}`;
            }
            if (!!filtros.fi) {
                end += `&fi=${filtros.fi}`;
            }
            if (!!filtros.ff) {
                end += `&ff=${filtros.ff}`;
            }
            if (!!filtros.scale) {
                end += `&scale=${filtros.scale}`;
            }
            if (!!filtros.gi) {
                end += `&gi=${filtros.gi}`;
            }
            if (!!filtros.gg) {
                end += `&gg=${filtros.gg}`;
            }

            miAxios.get(end)
            .then(res => {
                const { grupos, paginas } = res.data;

                u2('app', 'paginador', 'paginas', paginas);

                let cats = {};
                Object.keys(grupos).forEach(k => {
                    const grupo = grupos[k];
                    grupo.forEach(i => {
                        if (!cats[i.group_image]) {
                            cats[i.group_image] = [];
                        }
                        const cs = i.categorias || [];
                        cs.forEach(c => {
                            const added = cats[i.group_image].filter(cat => cat.nombre === c.nombre);
                            if (added.length === 0) {
                                cats[i.group_image].push(c);
                            }
                        });
                    });
                });
                // console.log(cats);
                // console.log(grupos);
                const originales = Object.keys(grupos).map(k => {
                    const grupo = grupos[k];
                    // console.log(cats, k, grupo);
                    let ng = grupo.filter(i => i.model === 'Original')[0];
                    if (!ng) {
                        ng = grupo[0];
                    }
                    ng.categorias = cats[k];
                    return ng;
                })

                // console.log(originales);
                u2('app', 'data', 'grupos', grupos);
                u2('app', 'data', 'originales', originales);
            })
            .catch(err => {
                console.log(err);
            }).finally(() => {
                u2('loaders', 'app', 'getImages', false);
            });
        },
        getGroupImages: grupo => {
            if (!!s.loaders?.app?.getGroupImages) return;

            u2('loaders', 'app', 'getGroupImages', true);

            const end = `app/get_image_group/?gi=${grupo}`;
            const data = { grupo };
            miAxios.get(end)
            .then(res => {
                const images = res.data.info
                u2('app', 'show', 'images', images);
            })
            .catch(err => {
                console.log(err);
            }).finally(() => {
                u2('loaders', 'app', 'getGroupImages', false);
            });
        },
        validateUrl: (url, setUrl) => {
            // view if url return 200
            miAxios.get(url)
            .then(res => {
                setUrl(url);
            })
            .catch(err => {
                console.log(err);
                setUrl('https://ojitos369.com/media/ojitos369/upload_gif.gif');
            });
        }
    }

    const update = {
        updateNew: form => {
            if (s.loaders?.update?.updateNew) return;

            u2('loaders', 'update', 'updateNew', true);
            const end = 'app/create_image_upscale/';
            const headers = {
                'Connection': 'keep-alive',
            };
            // timeout: 5 minutes
            miAxios.post(end, form, { headers, timeout: 600000 })
            .then(res => {
                const { message } = res.data;
                u1('update', 'form', {});
                const file_input = document.getElementById('update_file');
                file_input.value = '';

                MySwal.fire({
                    title: 'Update',
                    text: message,
                    icon: 'success',
                    confirmButtonText: 'Ok'
                });
            })
            .catch(err => {
                console.log(err);
                const { message } = err.response.data;
                MySwal.fire({
                    title: 'Update',
                    text: message,
                    icon: 'error',
                    confirmButtonText: 'Ok'
                });
            })
            .finally(() => {
                u2('loaders', 'update', 'updateNew', false);
            });
        },
    }

    // u[0-9]
    const u0 = (f0, value) => {
        d(ff.u0({f0, value}));
    }
    const u1 = (f0, f1, value) => {
        d(ff.u1({f0, f1, value}));
    }
    const u2 = (f0, f1, f2, value) => {
        d(ff.u2({f0, f1, f2, value}));
    }
    const u3 = (f0, f1, f2, f3, value) => {
        d(ff.u3({f0, f1, f2, f3, value}));
    }
    const u4 = (f0, f1, f2, f3, f4, value) => {
        d(ff.u4({f0, f1, f2, f3, f4, value}));
    }
    const u5 = (f0, f1, f2, f3, f4, f5, value) => {
        d(ff.u5({f0, f1, f2, f3, f4, f5, value}));
    }
    const u6 = (f0, f1, f2, f3, f4, f5, f6, value) => {
        d(ff.u6({f0, f1, f2, f3, f4, f5, f6, value}));
    }
    const u7 = (f0, f1, f2, f3, f4, f5, f6, f7, value) => {
        d(ff.u7({f0, f1, f2, f3, f4, f5, f6, f7, value}));
    }
    const u8 = (f0, f1, f2, f3, f4, f5, f6, f7, f8, value) => {
        d(ff.u8({f0, f1, f2, f3, f4, f5, f6, f7, f8, value}));
    }
    const u9 = (f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, value) => {
        d(ff.u9({f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, value}));
    }

    return { u0, u1, u2, u3, u4, u5, u6, u7, u8, u9, app, login, update };
}

export { useF };