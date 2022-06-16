product_id=self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
if product_id:
    config_image_path = self._notice['target']['config']['image_product'].rstrip('/') if not self._notice['target'][
    'config'].get('site_id') else self._notice['target']['config']['image_product'].rstrip(
    '/') + '/sites/' + to_str(self._notice['target']['config']['site_id'])
    if convert['thumb_image']['url'] or convert['thumb_image']['path']:
        image_process = self.process_image_before_import(convert['thumb_image']['url'],
                                                        convert['thumb_image']['path'])
        rf_path = self.get_map_field_by_src(self.TYPE_PATH_IMAGE, None, image_process['url'], field='code_desc')
        if not rf_path:
            image_import_path = self.uploadImageConnector(image_process, self.add_prefix_path(
            self.make_woocommerce_image_path(image_process['path']), config_image_path))

            if image_import_path:
                product_image = self.remove_prefix_path(image_import_path,
                                                        self._notice['target']['config']['image_product'])
                _, image_details = self.get_sizes(image_process['url'])
                # wp_image(self, path, image_details = None, label = '', convert = dict, check_exist=True)
                trid = self.get_new_trid()
                for lang_code, lang_name in self._notice['target']['languages'].items():
                    thumbnail_id = self.wp_image(product_image, image_details, convert['thumb_image'].get('label', ''),
                                                check_exist=False, lang=lang_code)
                    if thumbnail_id :
                        res = self.import_data_connector(self.rf_get_query_img_wpml(thumbnail_id, lang_code, trid))
                        self.log(thumbnail_id,"thumbnail_id")
                        product_meta = {
                            'meta_value': thumbnail_id,
                        }
                        where={
                        'post_id': product_id,
                        'meta_key':"_thumbnail_id"

                        }
                        update_query = self.create_update_query_connector("postmeta", product_meta,where)

                        product_update = self.import_product_data_connector(update_query, True, product_id)
