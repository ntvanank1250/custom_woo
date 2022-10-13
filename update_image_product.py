        product_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'],lang=self._notice['target']['language_default'])
		if product_id:
            ## get thumbnail target: 
            if convert['thumb_image']['url'] or convert['thumb_image']['path']:
                get_data_postmeta_where = {
                    "post_id":product_id,
                    "meta_key":"_thumbnail_id"
                }
                get_thumbnail = self.import_data_connector(self.create_select_query_connector("postmeta", get_data_postmeta_where))
                get_thumbnail = get_thumbnail[0]['meta_value']
                self.log(get_thumbnail,"get_thumbnail")
                if not get_thumbnail and get_thumbnail =='':
                    config_image_path = self._notice['target']['config']['image_product'].rstrip('/') if not self._notice['target'][
                    'config'].get('site_id') else self._notice['target']['config']['image_product'].rstrip(
                    '/') + '/sites/' + to_str(self._notice['target']['config']['site_id'])
                    image_process = self.process_image_before_import(convert['thumb_image']['url'],
                                                                    convert['thumb_image']['path'])
                    image_import_path = self.uploadImageConnector(image_process, self.add_prefix_path(
                        self.make_woocommerce_image_path(image_process['path']), config_image_path))

                    if image_import_path:
                        product_image = self.remove_prefix_path(image_import_path,
                                                                self._notice['target']['config']['image_product'])
                        _, image_details = self.get_sizes(image_process['url'])
                        thumbnail_id = self.wp_image(product_image, image_details, convert['thumb_image'].get('label', ''))

                        self.log(thumbnail_id,"thumbnail_id1")
                        product_meta = {
                            'meta_value': thumbnail_id,
                        }
                        where={
                        'post_id': product_id,
                        'meta_key':"_thumbnail_id"
                        }
                        update_query = self.import_data_connector(self.create_update_query_connector("postmeta", product_meta, where))
            if convert['images']:
                ## get image target: 
                get_data_postmeta_where = {
                    "post_id":product_id,
                    "meta_key":"_product_image_gallery"
                }
                get_gallery = self.import_data_connector(self.create_select_query_connector("postmeta", get_data_postmeta_where))
                get_gallery = get_gallery[0]['meta_value']
                self.log(get_gallery,"get_gallery")
                if not get_gallery and get_gallery =='':
                    gallery_meta_value = ''
                    gallery_ids = list()
                    for image in convert['images']:
                        image_process = self.process_image_before_import(image['url'], image['path'])
                        image_import_path = self.uploadImageConnector(image_process, self.add_prefix_path(
                            self.make_woocommerce_image_path(image_process['path']), config_image_path))
                        if image_import_path:
                            product_image = self.remove_prefix_path(image_import_path,
                                                                    self._notice['target']['config']['image_product'])
                            _, image_details = self.get_sizes(image_process['url'])
                            img_id = self.wp_image(product_image, image_details, image['label'])
                            if img_id:
                                gallery_ids.append(img_id)
                    gallery_meta_value = ','.join(str(id) for id in gallery_ids)
                    if gallery_meta_value:
                        self.log(gallery_meta_value,"gallery_meta_value")
                        product_meta = {
                            'meta_value': gallery_meta_value,
                        }
                        where={
                        'post_id': product_id,
                        'meta_key':"_product_image_gallery"
                        }
                        update_query = self.import_data_connector(self.create_update_query_connector("postmeta", product_meta, where))
